# AGENTS.md — Supabase Recon

Ponto de entrada para agentes Cursor/LLM neste repositorio.

## Idioma e ambiente

- Respostas e commits em **PT-BR**
- Terminal/scripts: **WSL Linux** (nunca CMD/PowerShell nativo)
- Sem emojis em codigo, logs ou docs tecnicos
- Sem comentarios no codigo (docstrings OK)

## Universo operacional

- Dominio: recon de apps **Lovable/Supabase** (bundles JS → Auth/REST/RPC/Edge, OpenAPI, teste com anon key)
- Arquitetura: DDD hexagonal (`domain` / `application` / `infrastructure` / `presentation`)
- SSOT de config: `.env` + `.env.example` (`docs/engineering-settings-ssot.md`)
- Composition root: `presentation/cli/bootstrap.py`
- Qualidade: `make help`, `app-lint` / `app-test` / `app-security` / `app-pre-commit-run` via `clean_workspace.py`

## O que o LLM e / nao e

- **E:** copiloto de engenharia e auditoria
- **Nao e:** autorizacao para atacar alvos sem permissao; gerador de exploits fora do analyzer

Doutrina: [`docs/llm-doctrine.md`](docs/llm-doctrine.md)
Matriz 100% cobertura: [`docs/agent-coverage.md`](docs/agent-coverage.md)
Rules/skills versionadas: [`.cursor/rules/`](.cursor/rules/) e [`.cursor/skills/`](.cursor/skills/)

## Proibicoes globais

- `domain`/`application` importando `infrastructure` ou `presentation`
- Logs em entidade ou use case; dump de secrets/payload em INFO
- Arquivos `app/src/**/*.py` acima de **300** linhas
- Cobertura de testes abaixo de **100%** (branch)
- Commitar `.env` ou tokens
- Assunto de commit em ingles; tipo/escopo fora do commitlint
- Afrouxar QA para “passar o hook”

## Escopos commitlint

`all`, `app`, `bundle`, `cli`, `config`, `deps`, `domain`, `infra`, `regex`, `repo`, `swagger`, `test`, `tester`, `linters`

Formato: `tipo(escopo): assunto em PT-BR` (escopo opcional). Tipos: build, chore, ci, docs, feat, fix, perf, qa, refactor, revert, style, test.

## Pre-commit

`linters/pre-commit-config.yaml` → `clean_workspace.py` stages: lint, test (cov 100%), security, cleanup; commit-msg: commitlint.

## Leitura por tarefa

| Tarefa | Abrir primeiro |
|--------|----------------|
| Qualquer mudanca | este arquivo + `docs/agent-coverage.md` |
| QA / pre-commit | `docs/engineering-standards.md` + skill `recon-precommit` |
| Fechamento de mudanca | `docs/engineering-surface-sync.md` + skill `recon-surface-sync` |
| Domain / ports | `docs/arquitetura.md` + `docs/structure.md` |
| Logging | `docs/engineering-logging.md` |
| Settings / `.env` | `docs/engineering-settings-ssot.md` + skill `recon-settings-change` |
| Analyze pipeline | skill `recon-analyze-debug` |
| Bundle / swagger | skill `recon-bundle-parse` |
| Reliability tests | skill `recon-reliability-test` |
| HTTP adapter | skill `recon-http-adapter` |
| Deps Python | `docs/engineering-python-deps.md` + skill `recon-python-deps` |
| Higienizacao | `docs/engineering-repo-hygiene.md` + skill `recon-repo-hygiene` |
| Make / CLI ops | skill `recon-ops-runbook` |
| Scaffold / contrato | `prompt-model.md` + skill `recon-surface-sync` |

Inventario: [`docs/structure.md`](docs/structure.md)
Arquitetura: [`docs/arquitetura.md`](docs/arquitetura.md)
