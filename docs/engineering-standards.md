# Padroes de engenharia e QA

## Gates obrigatorios

Orquestrador unico: `app/scripts/operations/clean_workspace.py`.

| Gate | Comando | Intencao |
|------|---------|----------|
| Lint | `make app-lint` | Python lint+validate (YAML/JSON incluidos) |
| Test | `make app-test` | pytest + coverage branch fail-under 100 |
| Security | `make app-security` | bandit + pip-audit + Gitleaks (se no PATH) |
| Setup | `make app-setup` | install + hooks pre-commit/commit-msg |
| Hooks all | `make app-pre-commit-run` | pre-commit run --all-files |

Ajuda: `make help`.

Pre-commit (`linters/pre-commit-config.yaml`): commitlint primeiro; Python | Lint, Seguranca, Testes, Validate, Build; YAML/JSON no lint/validate Python.

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
- Perfil sênior / AppSec: skill `recon-senior-appsec` + [`engineering-senior-profile.md`](engineering-senior-profile.md)
- CI / release: skill `recon-ci-release` + [`engineering-ci-release.md`](engineering-ci-release.md)
- Onboarding: skill `recon-course-senior` + [`courses/senior-appsec-path.md`](courses/senior-appsec-path.md)
