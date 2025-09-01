FROM mcr.microsoft.com/devcontainers/javascript-node:20-bookworm

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
        && apt-get -y install --no-install-recommends \
        # Pandoc and document processing (citeproc is now built-in)
        pandoc \
        # Complete LaTeX installation (includes all packages we need)
        texlive-full \
        # Additional fonts for better typography
        fonts-liberation \
        fonts-liberation2 \
        fonts-noto \
        fonts-noto-cjk \
        fonts-firacode \
        # Image processing for diagrams
        librsvg2-bin \
        imagemagick \
        # Python for pandoc filters
        python3-pip \
        python3-setuptools \
        # Build tools
        make \
        # Utilities
        jq \
        curl \
        wget \
        zip \
        # FOLLOWING: support for finding packages
        apt-file \
        # PDF utilities
        poppler-utils \
        ghostscript \
        # File watching
        inotify-tools \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Install Python packages for pandoc filters
RUN pip3 install --no-cache-dir --break-system-packages \
        pandoc-include \
        pandoc-plantuml-filter \
        pandoc-mustache \
        panflute \
        pypandoc \
        weasyprint

# Install minimal global npm packages (ARM64 compatible)
RUN npm install -g \
        markdownlint-cli \
        prettier \
        serve

# Template directory will be populated from local templates/ folder
RUN mkdir -p /usr/share/pandoc/data/templates

# Copy eisvogel template to Pandoc's directory for cascading support
COPY templates/eisvogel.latex /usr/share/pandoc/data/templates/

# Note: Chrome/Puppeteer not installed to avoid ARM64 compatibility issues
# PDF generation relies on pandoc + LaTeX for professional output

# Create working directories
WORKDIR /workspace
RUN mkdir -p \
        inbox \
        outbox \
        templates \
        scripts \
        output \
        logs \
        config

# Set up template directory with proper permissions
RUN chown -R node:node /workspace

# Switch to node user
USER node

# Set environment variables
ENV NODE_ENV=development \
        PDF_ENGINE=xelatex \
        PANDOC_DATA_DIR=/usr/share/pandoc/data
