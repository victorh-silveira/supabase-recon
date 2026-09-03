# Matriz de cobertura do agente (100%)

Cada superficie do analyzer tem **doc + rule + skill** (ou `—` justificado). Entrada: [`AGENTS.md`](../AGENTS.md).

Rules/skills vivem em [`.cursor/`](../.cursor/) e sao **versionadas** no git.

## Matriz

| Superficie | Doc | Rule (`.cursor/rules/`) | Skill (`.cursor/skills/`) |
|------------|-----|-------------------------|---------------------------|
| Doutrina LLM | [llm-doctrine.md](llm-doctrine.md) | `recon-llm-doctrine.mdc` | `recon-surface-sync` |
| Perfil sênior | [engineering-senior-profile.md](engineering-senior-profile.md) | `recon-senior-profile.mdc` | `recon-senior-appsec` |
| Personas / agentes | [agents/README.md](agents/README.md) | `recon-senior-profile.mdc` | `recon-course-senior` |
| Curso sênior | [courses/senior-appsec-path.md](courses/senior-appsec-path.md) | `recon-senior-profile.mdc` | `recon-course-senior` |
| Engenharia / QA | [engineering-standards.md](engineering-standards.md) | `recon-engineering.mdc` + `recon-testing.mdc` | `recon-precommit` |
| Domain puro | [arquitetura.md](arquitetura.md) + [structure.md](structure.md) | `recon-domain-pure.mdc` | — |
| Hexagonal / ports | [arquitetura.md](arquitetura.md) + [structure.md](structure.md) | `recon-hexagonal.mdc` | `recon-analyze-debug` |
| Logging | [engineering-logging.md](engineering-logging.md) | `recon-logging.mdc` | `recon-analyze-debug` |
| HTTP / YAML security | [engineering-http-yaml-security.md](engineering-http-yaml-security.md) | `recon-http-yaml-security.mdc` | `recon-http-adapter` |
| Presentation / Rich | [engineering-http-yaml-security.md](engineering-http-yaml-security.md) | `recon-presentation-rich.mdc` | `recon-senior-appsec` |
| CI / release | [engineering-ci-release.md](engineering-ci-release.md) | `recon-ci-release.mdc` | `recon-ci-release` |
| Settings / `.env` | [engineering-settings-ssot.md](engineering-settings-ssot.md) | `recon-settings-ssot.mdc` | `recon-settings-change` |
| Deps Python | [engineering-python-deps.md](engineering-python-deps.md) | `recon-python-deps.mdc` | `recon-python-deps` |
| Higienizacao | [engineering-repo-hygiene.md](engineering-repo-hygiene.md) | `recon-repo-hygiene.mdc` | `recon-repo-hygiene` |
| Surface sync | [engineering-surface-sync.md](engineering-surface-sync.md) | `recon-surface-sync.mdc` | `recon-surface-sync` |
| Contrato prompt-modelo | [prompt-model.md](../prompt-model.md) | `recon-engineering.mdc` | `recon-surface-sync` |
| Scripts / Make | [engineering-python.md](engineering-python.md) + [structure.md](structure.md) | `recon-scripts.mdc` | `recon-ops-runbook` |
| CLI / bootstrap | [engineering-python.md](engineering-python.md) | `recon-cli.mdc` | `recon-ops-runbook` |
| Analyze pipeline | [arquitetura.md](arquitetura.md) | `recon-hexagonal.mdc` | `recon-analyze-debug` |
| Bundle / swagger | [arquitetura.md](arquitetura.md) | `recon-domain-pure.mdc` | `recon-bundle-parse` |
| Reliability tests | [arquitetura.md](arquitetura.md) | `recon-testing.mdc` | `recon-reliability-test` |
| HTTP adapter | [engineering-logging.md](engineering-logging.md) + [engineering-http-yaml-security.md](engineering-http-yaml-security.md) | `recon-hexagonal.mdc` + `recon-http-yaml-security.mdc` | `recon-http-adapter` |

## Pastas DDD ↔ matriz

| Pasta | Linha da matriz |
|-------|-----------------|
| `app/src/domain/` | Domain puro + Bundle / swagger |
| `app/src/application/ports/` | Hexagonal / ports |
| `app/src/application/use_cases/` | Analyze pipeline + Reliability tests |
| `app/src/infrastructure/adapters/` | HTTP adapter |
| `app/src/infrastructure/config/` | Settings / `.env` |
| `app/src/infrastructure/logging/` | Logging |
| `app/src/presentation/` | CLI / bootstrap + Logging |
| `app/scripts/operations/` | Scripts / Make |
| `app/tests/` | Engenharia / QA |
| `.env.example` | Settings / `.env` |

## Rules alwaysApply

Todas as rules em `.cursor/rules/*.mdc` usam `alwaysApply: true`.
