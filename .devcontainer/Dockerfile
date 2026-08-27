# Derived dev image for P2-Knowledge-Base.
#
# Bakes ALL container tooling into cached layers so it survives rebuilds/recreates
# and works offline. NEVER install at runtime or in postCreateCommand — baked
# layers are the only persistent path. postCreateCommand is reserved for the few
# steps that genuinely depend on runtime mounts (see devcontainer.json).
#
# Baked here: native PDF engines + full PDF->Markdown toolkit (docling, etc.),
# Node.js LTS + @openai/codex, the pnut-ts P2 compiler, the Claude CLI, and PyYAML
# for the repo's python validation scripts.
FROM mcr.microsoft.com/devcontainers/python:3.12

# --- git: trust the workspace bind mount -------------------------------------
# The workspace arrives over a virtiofs bind mount whose uid attribution is
# occasionally transient -- the same path can report uid 1000 one moment and a
# different uid the next with nothing changed on disk. Git's ownership check
# then refuses with "detected dubious ownership" and every git query in the tree
# fails. Intermittently, which is worse than always: it makes gates that
# discover their inputs with `git ls-files` report green having read nothing.
#
# System scope, because ~/.gitconfig is a READ-ONLY bind mount. Git writes
# config by rename, so `git config --global` there fails with EBUSY -- the
# remedy git itself prints cannot be applied in this container. /etc/gitconfig
# is root-owned, baked, and survives rebuilds. VS Code appends its credential
# helper to the same file at container start; the two coexist.
#
# Scoped to /workspaces/* rather than '*' so the check stays live elsewhere.
# A trailing /* matches at any depth.
RUN git config --system --add safe.directory '/workspaces/*'

# Pre-fetched docling models live in the image; point docling at them so first
# conversion is offline and rebuild-stable regardless of the runtime user/home.
ENV DOCLING_ARTIFACTS_PATH=/opt/pdf-tools/models \
    HF_HOME=/opt/pdf-tools/hf-cache

# --- native engines (poppler/mupdf/tesseract/ghostscript), opencv + build deps --
# The base image ships a yarn apt repo whose signing key fails verification on
# Debian trixie's strict verifier — drop it before any apt-get update so it can't
# abort the build. We don't need it (Node comes from NodeSource below; add yarn
# via `npm i -g yarn` if ever required).
RUN grep -rIl 'dl\.yarnpkg\.com' /etc/apt 2>/dev/null | xargs -r rm -f; \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        poppler-utils \
        mupdf-tools \
        ghostscript \
        tesseract-ocr tesseract-ocr-eng \
        qpdf \
        libgl1 libglib2.0-0 \
        unzip ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*

# --- Node.js LTS (replaces the devcontainer node feature so npm globals bake) ----
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @openai/codex \
    && rm -rf /var/lib/apt/lists/*

# --- pnut-ts compiler --------------------------------------------------------
# *** THE VERSION IS DISCOVERED, NOT TYPED. ***
# It used to be spelled out in three places -- the COPY, the cp path and the rm --
# so dropping a newer zip in and rebuilding silently rebuilt the OLD compiler,
# with nothing anywhere reporting which one you got. The glob takes every zip
# present and the sort picks the highest version, so adding a zip is the whole
# upgrade. The chosen version is echoed into the build log, and `pnut-ts
# --version` is run as a build-time smoke test so a bad binary fails the layer
# rather than the first compile that needs it.
#
# NOTE: the zip baked here is linux-arm64 (Apple Silicon host). Re-point the
# COPY glob if building on an x64 host.
COPY pnut-ts-linux-arm64-*.zip /tmp/pnut/
RUN cd /tmp/pnut \
    && ZIP="$(ls pnut-ts-linux-arm64-*.zip | sort -V | tail -1)" \
    && echo "Baking pnut-ts from ${ZIP}" \
    && unzip -oq "$ZIP" \
    && cp "${ZIP%.zip}/pnut_ts/pnut-ts" /usr/local/bin/pnut-ts \
    && chmod +x /usr/local/bin/pnut-ts \
    && mkdir -p /opt/pnut-ts-docs \
    && find "${ZIP%.zip}/pnut_ts" -maxdepth 1 -type f \
         ! -name 'pnut-ts' ! -name 'pnut_ts' -exec cp {} /opt/pnut-ts-docs/ \; \
    && cd / && rm -rf /tmp/pnut \
    && pnut-ts --version

# --- isolated venv with the full PDF extraction bundle (docling pulls torch ~GB) -
RUN python3 -m venv /opt/pdf-tools/venv \
    && /opt/pdf-tools/venv/bin/pip install --no-cache-dir --upgrade pip wheel \
    && /opt/pdf-tools/venv/bin/pip install --no-cache-dir \
        docling \
        pymupdf pymupdf4llm \
        pdfplumber \
        "camelot-py[cv]" \
        ocrmypdf

# --- pre-fetch docling models into the baked artifacts path --------------------
RUN /opt/pdf-tools/venv/bin/docling-tools models download -o /opt/pdf-tools/models || true

# --- on-PATH wrapper commands (agent calls these; no venv knowledge needed) -----
RUN printf '%s\n' '#!/usr/bin/env bash' 'exec /opt/pdf-tools/venv/bin/docling --to md "$@"' > /usr/local/bin/pdf2md \
    && printf '%s\n' '#!/usr/bin/env bash' 'exec pdftotext -layout "$@" -' > /usr/local/bin/pdf-layout \
    && printf '%s\n' '#!/usr/bin/env bash' 'exec /opt/pdf-tools/venv/bin/ocrmypdf "$@"' > /usr/local/bin/pdf-ocr \
    && ln -sfn /opt/pdf-tools/venv/bin/docling /usr/local/bin/docling \
    && ln -sfn /opt/pdf-tools/venv/bin/camelot /usr/local/bin/camelot \
    && chmod +x /usr/local/bin/pdf2md /usr/local/bin/pdf-layout /usr/local/bin/pdf-ocr \
    && chmod -R a+rX /opt/pdf-tools

# --- reference doc for humans --------------------------------------------------
RUN printf '%s\n' \
    '# PDF -> text/Markdown tools (baked by .devcontainer/Dockerfile)' \
    '' \
    'Most KB PDFs are digitally generated (real text layer) — skip OCR unless a page is scanned.' \
    '' \
    '- pdf2md <file.pdf>        : best fidelity -> Markdown (tables + fenced code). [docling]' \
    '- pdf-layout <file.pdf>    : plain text preserving indentation, for PASM2/Spin2 listings. [pdftotext -layout]' \
    '- camelot lattice -p all -f csv -o <out.csv> <file.pdf> : surgical ruled-table -> CSV.' \
    '  (options belong to the SUBCOMMAND; `camelot --pages ...` is rejected with exit 2.)' \
    '- pdf-ocr <in.pdf> <out.pdf> : OCR a scanned PDF, then run pdf2md on the output. [ocrmypdf]' \
    '' \
    'Venv: /opt/pdf-tools/venv   Models: /opt/pdf-tools/models (DOCLING_ARTIFACTS_PATH)' \
    > /opt/pdf-tools/README.md

# --- per-user tooling baked into the image (Claude CLI + repo tooling deps) -----
# Installed as the runtime user so it lands in /home/vscode and is on PATH.
# These are what engineering/tools/ runs under the SYSTEM python3. Note pymupdf is
# also in /opt/pdf-tools/venv above, but that venv is isolated -- the validation
# gates import it as plain `fitz`, so it must exist here too or they fail closed
# ("PyMuPDF is required") mid-release. audit-pdf-margin-overflow.py hit exactly that
# in a fresh container on 2026-08-21.
USER vscode
RUN curl -fsSL https://claude.ai/install.sh | bash \
    && grep -q '\.local/bin' ~/.bashrc 2>/dev/null \
       || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc \
    && pip install --user --no-cache-dir PyYAML pymupdf
USER root
