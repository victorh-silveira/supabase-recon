---
name: recon-ops-runbook
description: >-
  Operates supabase-recon via Make targets and CLI entrypoints on WSL. Use when
  setting up the env, running analysis, or the user mentions make help,
  app-setup, app-run, app-pre-commit-run, or how to execute the tool.
---

# Ops runbook

## Comandos

```bash
make help
make app-setup
make app-run ARGS="--url https://exemplo.app"
make app-lint && make app-test && make app-security
make app-pre-commit-run
```

Entrypoint: `python run.py --url ...` (`--skip-download`, `--no-test`, `--methods`).

Python do Make: `.venv/bin/python` se existir.

## Docs

`README.md`, `docs/engineering-python.md`, rule `recon-scripts` + `recon-cli`
