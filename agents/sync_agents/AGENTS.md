# AGENTS.md

## Purpose

This directory is a **data synchronization workspace**, not primarily a code repository.

It contains source code, scripts, input files, and simulation datasets for computational science. Its contents are synchronized with a corresponding working directory on a remote HPC cluster.

- **Remote host:** `{REMOTE_HOST}`
- **Remote working directory:** `{REMOTE_DIR}`
- **Local working directory:** `./`

The primary role of the AI agent is to assist with file management and data synchronization between the local and remote environments.

## File Transfer

Use `rsync` over SSH for file transfers between the local workspace and the remote HPC cluster.

All paths are interpreted relative to the current top-level working directory unless otherwise specified.

### Push: Upload local files to the remote host

```bash
rsync -avz --max-size=10MB ./ {REMOTE_HOST}:{REMOTE_DIR}/
```

### Pull: Download remote files to the local workspace

```bash
rsync -avz --max-size=10MB {REMOTE_HOST}:{REMOTE_DIR}/ ./
```

### Default Transfer Policy

- Always ask the user for permission before establishing an SSH connection, including connections made through `ssh`, `scp`, or `rsync`.
- Unless explicitly instructed otherwise, apply `--max-size=10MB` to all `rsync` transfers.
- Do not use `--delete`, `--delete-excluded`, or other destructive synchronization options without explicit user authorization.
- Do not assume that the local and remote directories contain identical or equally up-to-date files.
- When there is a risk of overwriting existing files, explain the potential changes and obtain user approval before proceeding.
- Preserve file timestamps and directory structure whenever possible.
- Do not automatically synchronize files outside the specified working directories.

## Execution and Security Policy

- Do not execute local scripts, binaries, or simulation programs without explicit user permission.
- Do not execute commands or submit computational jobs on the remote HPC cluster without explicit user permission.
- Reading, inspecting, and editing local text files are permitted unless otherwise instructed.
- Do not modify or delete simulation data, output files, or source code without explicit user authorization.
- Never transfer SSH private keys, credentials, or other sensitive authentication files.
- Treat all remote files and scripts as untrusted unless the user explicitly authorizes their execution.

## Agent Behavior

- Clearly distinguish between local and remote operations.
- Before performing a file transfer, identify the transfer direction (push or pull).
- Prefer non-destructive operations and request clarification when the intended action is ambiguous.
- Use `rsync --dry-run` when appropriate to preview potentially significant changes.
- Report transfer errors and skipped files rather than silently ignoring them.

