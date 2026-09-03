---
name: recon-precommit
description: >-
  Diagnoses and fixes supabase-recon pre-commit failures (commitlint first,
  Python lint/security/test/validate/build with YAML/JSON inside Python stages,
  300-line limit, pytest branch coverage 100%). Use when pre-commit fails,
  coverage drops, a file exceeds 300 lines, or the user mentions
  clean_workspace, fail-under, or commitlint.
---

# Pre-commit supabase-recon

Crash-first no stage `commit-msg` (`fail_fast: true`): commitlint → Python | Lint → Seguranca → Testes → Validate → Build → limpeza.

YAML/JSON entram em Python | Lint e Python | Validate (nao sao stacks). Mensagem invalida aborta antes dos gates Python.

## Passos

1. Ler o trecho FAIL do hook
2. Commitlint: tipo+escopo validos; assunto PT-BR (primeiro do crash-first)
3. Python | Lint: Ruff, Interrogate, Vulture, yamllint, JSON parse
4. Python | Seguranca: Bandit, pip-audit, Gitleaks se estiver no PATH
5. Python | Testes: reproduzir o teste; cobrir misses/branches
6. Python | Validate: mypy, camadas, 300 linhas, `yaml.safe_load`, JSON estrutural
7. Python | Build: `compileall`
8. Reexecutar no **WSL**: `make app-lint` / `make app-test` / `make app-security` (ou `make app-pre-commit-run`)

## Docs

`docs/engineering-standards.md`, `docs/engineering-ci-release.md`, `AGENTS.md`
