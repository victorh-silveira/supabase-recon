# Padroes de engenharia e QA

## Gates obrigatorios

Orquestrador unico: `app/scripts/operations/clean_workspace.py`.

| Gate | Comando | Intencao |
|------|---------|----------|
| Lint | `make app-lint` | Ruff, interrogate, vulture, mypy strict, deps entre camadas, max 300 linhas |
| Test | `make app-test` | pytest + coverage branch fail-under 100 |
| Security | `make app-security` | bandit + pip-audit |
| Setup | `make app-setup` | install + hooks pre-commit/commit-msg |
| Hooks all | `make app-pre-commit-run` | pre-commit run --all-files |

Ajuda: `make help`.

Pre-commit (`linters/pre-commit-config.yaml`) chama os mesmos stages + commitlint.

## Invariantes

- `app/src/**/*.py` <= 300 linhas
- Cobertura 100% com branch coverage nas camadas de app
- Sem comentarios no codigo (docstrings OK)
- Docs PT-BR; sem emojis
- Conventional Commits: `tipo(escopo): assunto PT-BR` (escopos em `linters/commitlint.config.mjs`)
- Terminal/scripts: WSL Linux

## Camadas

Ver [`structure.md`](structure.md) e [`arquitetura.md`](arquitetura.md). Gate de imports impede `domain`/`application` de importar `infrastructure`/`presentation`.

## Skills

- Falha de hook: skill `recon-precommit`
- Fechamento de mudanca: skill `recon-surface-sync`
