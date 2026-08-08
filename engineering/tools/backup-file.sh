#!/usr/bin/env bash
#
# backup-file.sh — the ONE way to make a safety copy in this workspace.
#
# Sacred Rule #1 requires a timestamped backup before modifying a large or
# important file. Saying "make a timestamped backup" in prose produced eight
# different naming shapes and fifteen .gitignore rules chasing them. This
# script makes the rule executable so it cannot drift again.
#
# Every backup lands in ONE place, mirroring its repo-relative path:
#
#     .backups/<repo-relative-path>.<YYYYMMDD-HHMMSS>
#
# which is covered by a single .gitignore line (/.backups/). Backups therefore
# never sit beside the file they copy, so they can never be picked up by a
# grep, glob, find, audit script, or source-selection step. That failure mode
# is not hypothetical: backup files adjacent to the DeSilva opus-masters were
# once mistaken for the live source.
#
# Usage:
#   engineering/tools/backup-file.sh <path> [<path>...]   back up one or more files
#   engineering/tools/backup-file.sh --prune [DAYS]       delete backups older than DAYS (default 30)
#   engineering/tools/backup-file.sh --list               show what is currently held
#
# NOTE: for a tracked file, git history is the real backup — these copies only
# guard the window between an edit and its commit, so pruning is cheap.
#
# DO NOT back up a regenerable artifact (workspace renders rebuilt by
# prepare-manual, generated indexes, extracted text). The generator is the
# backup. This is what produced 222 of the 354 legacy backups found in the
# 2026-08-08 census.

set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
BACKUP_ROOT="$REPO_ROOT/.backups"

usage() { sed -n '2,40p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'; }

prune() {
    local days="${1:-30}"
    [ -d "$BACKUP_ROOT" ] || { echo "No .backups/ directory — nothing to prune."; return 0; }
    local count
    count=$(find "$BACKUP_ROOT" -type f -mtime "+$days" | wc -l)
    if [ "$count" -eq 0 ]; then
        echo "No backups older than $days days."
        return 0
    fi
    find "$BACKUP_ROOT" -type f -mtime "+$days" -delete
    find "$BACKUP_ROOT" -type d -empty -delete 2>/dev/null || true
    echo "Pruned $count backup(s) older than $days days."
}

list() {
    [ -d "$BACKUP_ROOT" ] || { echo "No .backups/ directory."; return 0; }
    local count size
    count=$(find "$BACKUP_ROOT" -type f | wc -l)
    size=$(du -sh "$BACKUP_ROOT" 2>/dev/null | cut -f1)
    echo "$count backup(s), $size, under $BACKUP_ROOT"
    find "$BACKUP_ROOT" -type f -printf '%T+  %P\n' 2>/dev/null | sort
}

backup_one() {
    local src="$1"

    if [ ! -f "$src" ]; then
        echo "ERROR: not a file: $src" >&2
        return 1
    fi

    # Repo-relative path, so the backup tree mirrors the working tree.
    local abs rel
    abs="$(cd "$(dirname "$src")" && pwd)/$(basename "$src")"
    case "$abs" in
        "$REPO_ROOT"/*) rel="${abs#"$REPO_ROOT"/}" ;;
        *) echo "ERROR: outside the repository: $src" >&2; return 1 ;;
    esac

    local stamp dest
    stamp="$(date +%Y%m%d-%H%M%S)"
    dest="$BACKUP_ROOT/$rel.$stamp"

    mkdir -p "$(dirname "$dest")"
    cp -p "$src" "$dest"
    echo "$dest"
}

case "${1:---help}" in
    --help|-h) usage ;;
    --prune)   prune "${2:-30}" ;;
    --list)    list ;;
    -*)        echo "ERROR: unknown option: $1" >&2; usage >&2; exit 2 ;;
    *)
        [ $# -ge 1 ] || { usage >&2; exit 2; }
        for f in "$@"; do backup_one "$f"; done
        ;;
esac
