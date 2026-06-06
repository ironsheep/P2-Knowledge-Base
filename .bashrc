#!/bin/bash
# Workspace shell customizations — appended to ~/.bashrc by the devcontainer postCreate.

# Claude Code path (installed via claude.ai/install.sh to ~/.local/bin)
if [ -d "$HOME/.local/bin" ] ; then
    export PATH="$HOME/.local/bin:$PATH"
fi

alias ll='ls -lG'
alias lsf='ls -FG'
alias myclaude='claude --dangerously-skip-permissions --verbose'
