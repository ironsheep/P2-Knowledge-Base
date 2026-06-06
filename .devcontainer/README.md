# P2 Knowledge Base Dev Container

This directory contains the VSCode Dev Container configuration for the P2 Knowledge Base project.

## Quick Start

1. **Install Prerequisites:**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [VSCode](https://code.visualstudio.com/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **PNut-TS Binary:**
   The Linux ARM64 `pnut-ts` compiler ships as a checked-in zip in this
   directory (`pnut-ts-linux-arm64-*.zip`) and is installed automatically
   by `postCreateCommand`. No manual step required.

3. **Open in Container:**
   - Open this repository in VSCode
   - Click "Reopen in Container" when prompted
   - OR: Command Palette → "Dev Containers: Reopen in Container"

## What's Included

### Base Image
- **Image:** `mcr.microsoft.com/devcontainers/python:3.12`
- **OS:** Debian-based (Ubuntu-like, uses `apt`)
- **Size:** ~500MB
- **User:** `vscode` (non-root with sudo access)

### Languages & Tools
- **Python 3.12** - Latest stable Python
- **Node.js LTS** - For MCP server development, Claude Code, Todo-MCP
- **npm** - Node package manager (included with Node.js)
- **Git** - Version control
- **Bash** - Default shell (configured in VSCode)

### Python Packages
- **PyYAML** - YAML processing (auto-installed)

### P2 Tools
- **PNut-TS** - P2 Spin2/PASM2 compiler
  - Location: `/usr/local/bin/pnut-ts` (in PATH)

### VSCode Extensions (Auto-installed)
- Python (ms-python.python)
- YAML (redhat.vscode-yaml)
- Markdown All in One (yzhang.markdown-all-in-one)
- GitLens (eamodio.gitlens)

## Directory Structure

```
.devcontainer/
├── devcontainer.json              # Main configuration
├── docker-compose.yml             # Base service (image + workspace mount)
├── docker-compose.override.yml    # Local-only mounts (gitignored)
├── pnut-ts-linux-arm64-*.zip      # Bundled P2 compiler (installed by postCreate)
└── README.md                      # This file
```

## PNut-TS Installation

During container creation, `postCreateCommand`:
1. Unzips the bundled `pnut-ts-linux-arm64-*.zip`
2. Copies the `pnut-ts` binary to `/usr/local/bin/pnut-ts`
3. Makes it executable with `chmod +x`

## Customization

### Add More Python Packages
Edit `postCreateCommand` in `devcontainer.json`:
```json
"postCreateCommand": "pip install --user PyYAML <package2> <package3> && ..."
```

### Add More VSCode Extensions
Add to `extensions` array in `devcontainer.json`:
```json
"extensions": [
  "ms-python.python",
  "your.extension.id"
]
```

### Install Additional Tools
Add to `postCreateCommand`:
```json
"postCreateCommand": "pip install --user PyYAML && sudo apt-get update && sudo apt-get install -y <package> && ..."
```

## Installing Node.js Tools

The container includes Node.js LTS and npm, ready for installing tools:

### Claude Code (AI Coding Assistant)
```bash
npm install -g @anthropic-ai/claude-code
```

### Todo-MCP (Task Management)
```bash
npm install -g @your-org/todo-mcp  # Adjust package name as needed
```

### Project MCP Server
```bash
cd engineering/enhancements/mcp-server
npm install
npm start
```

### Verify Node.js Setup
```bash
node --version   # Should show v20.x or v22.x (LTS)
npm --version    # Should show v10.x+
which npm        # Should show /usr/local/bin/npm or similar
```

## Troubleshooting

### PNut-TS Not Found
```bash
# Inside container, check:
ls -la /usr/local/bin/pnut-ts
which pnut-ts
pnut-ts --version
```

### Python Package Issues
```bash
# Inside container:
pip list | grep PyYAML
pip install --user --force-reinstall PyYAML
```

### Rebuild Container
If things get weird:
- Command Palette → "Dev Containers: Rebuild Container"
- This pulls fresh image and re-runs setup

## Performance Notes

**First Launch:**
- Pulls ~500MB image (once)
- Runs postCreateCommand (~30 seconds)
- Total: ~1-2 minutes

**Subsequent Launches:**
- Image cached locally
- Container starts in ~5 seconds

**Updates:**
- Rebuild container to get latest base image updates
- Microsoft updates the Python image regularly

## Security

- Container runs as non-root user (`vscode`)
- Sudo access available for installing packages
- Repository mounted as volume (changes persist)
- PNut-TS installed from a bundled zip during container creation

## Support

- **Dev Containers:** https://code.visualstudio.com/docs/devcontainers/containers
- **Base Image:** https://github.com/devcontainers/images/tree/main/src/python
- **Features:** https://containers.dev/features
