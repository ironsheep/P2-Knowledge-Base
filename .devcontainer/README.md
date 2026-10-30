# P2 Knowledge Base Dev Container

This directory contains the VS Code Dev Container configuration for the P2 Knowledge Base project.

## Quick Start

1. **Install prerequisites:**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Add the pnut-ts compiler zip:**
   The Dockerfile bakes the Linux ARM64 `pnut-ts` compiler from a
   `pnut-ts-linux-arm64-*.zip` placed in this directory. When several are
   present, the highest version is used.

3. **Open in the container:**
   - Open this repository in VS Code
   - Click "Reopen in Container" when prompted
   - Or: Command Palette → "Dev Containers: Reopen in Container"

## How the image is built

Before every open and rebuild, `initializeCommand` in `devcontainer.json` runs
`docker build` on the host and tags `p2-knowledge-base-dev:local`. The compose
service names that image and has no `build:` section: for a compose `build:`,
the Dev Containers extension builds from a generated Dockerfile in the host's
temp folder, which buildx 0.37.2 and later refuse to read.

Cached layers make the build about a second when nothing changed. *Rebuild
Without Cache* does not force a fresh build; to do that, run the `docker build`
line from `initializeCommand` with `--no-cache`, then Rebuild.

## What's included

All tooling is baked into the image by `Dockerfile`, so it survives rebuilds
and works offline.

- **Base image:** `mcr.microsoft.com/devcontainers/python:3.12`, user `vscode`
- **Python 3.12**, with PyYAML and PyMuPDF for the repo's validation scripts
- **Node.js 22 (LTS)** from NodeSource, with `@openai/codex`
- **pnut-ts**, the P2 Spin2/PASM2 compiler, at `/usr/local/bin/pnut-ts`
- **PDF toolkit:** `pdf2md` (docling), `pdf-layout` (pdftotext), `camelot`,
  `pdf-ocr` (ocrmypdf). Reference: `/opt/pdf-tools/README.md` in the container.
- **Git**, with the workspace trusted and identity baked into `/etc/gitconfig`

VS Code extensions installed in the container are listed in `devcontainer.json`.

## Directory structure

```
.devcontainer/
├── devcontainer.json                      # Main configuration; builds the image
├── Dockerfile                             # Everything baked into the image
├── docker-compose.yml                     # Service (image + workspace mount)
├── docker-compose.override.yml.example    # Template for local-only mounts
├── docker-compose.override.yml            # Local-only mounts (gitignored)
├── pnut-ts-linux-arm64-*.zip              # P2 compiler, baked by the Dockerfile
└── README.md                              # This file
```

## Local customization

- **Mounts** (for example `~/.ssh` for git over SSH): copy
  `docker-compose.override.yml.example` to `docker-compose.override.yml` and
  edit it. If the override is missing, an empty one is created so the
  container still starts.
- **Extra image layers:** put Dockerfile lines in
  `.devcontainer/Dockerfile.local-additions`. `initializeCommand` appends them
  to `Dockerfile` as `Dockerfile.local` and builds from that. Both files are
  gitignored.
- **Project tooling:** add it to `Dockerfile` so it is baked into the image,
  never to `postCreateCommand`.

## Troubleshooting

```bash
# Inside the container:
pnut-ts --version
node --version
python3 -c "import yaml, fitz; print('ok')"
```

If the image looks stale, run the `docker build` line from `initializeCommand`
with `--no-cache` on the host, then "Dev Containers: Rebuild Container".

## Support

- **Dev Containers:** https://code.visualstudio.com/docs/devcontainers/containers
- **Base image:** https://github.com/devcontainers/images/tree/main/src/python
