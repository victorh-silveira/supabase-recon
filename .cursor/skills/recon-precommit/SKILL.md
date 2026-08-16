---
name: recon-precommit
description: >-
  Diagnoses and fixes supabase-recon pre-commit failures (Ruff, Interrogate,
  Vulture, mypy, 300-line limit, pytest branch coverage 100%, Bandit, pip-audit,
  commitlint PT-BR). Use when pre-commit fails, coverage drops, a file exceeds
  300 lines, or the user mentions clean_workspace, fail-under, or commitlint.
---

# Pre-commit supabase-recon

## Passos

1. Ler o trecho FAIL do hook (lint / test / security / commitlint)
2. Lint: Ruff format/fix; Interrogate; Vulture; mypy strict; split se >300 linhas; deps entre camadas
3. Test: reproduzir o teste; cobrir misses/branches do report
4. Security: corrigir Bandit real; pip-audit com cuidado nos ignores
5. Commitlint: tipo+escopo validos; assunto PT-BR
6. Reexecutar no **WSL**: `make app-lint` / `make app-test` / `make app-security` (ou `make app-pre-commit-run`)

## Docs

`docs/engineering-standards.md`, `AGENTS.md`
