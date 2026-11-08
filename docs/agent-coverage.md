# Matriz de Cobertura do Agente de IA (100%)

Esta matriz estabelece a rastreabilidade bidirecional exaustiva entre todas as superfícies da aplicação, seus documentos de arquitetura, suas regras de governança e suas habilidades operacionais.

O ponto de entrada canônico do repositório é o [`AGENTS.md`](../AGENTS.md).
O harness canônico reside em [`.agents/`](../.agents/) (com retrocompatibilidade via [`.cursor/`](../.cursor/)) e é **versionado** no git.

---

## Matriz de Rastreabilidade

| Superfície | Documento de Referência | Regra Canônica (`.agents/rules/`) | Habilidade Operacional (`.agents/skills/`) |
|---|---|---|---|
| Doutrina e Ética LLM | [llm-doctrine.md](llm-doctrine.md) | `recon-llm-doctrine.mdc` | `recon-surface-sync` |
| Perfil Sênior de Engenharia | [engineering-senior-profile.md](engineering-senior-profile.md) | `recon-senior-profile.mdc` | `recon-senior-appsec` |
| Personas e Agentes | [agents/README.md](agents/README.md) | `recon-senior-profile.mdc` | `recon-course-senior` |
| Trilha de Formação Sênior | [courses/senior-appsec-path.md](courses/senior-appsec-path.md) | `recon-senior-profile.mdc` | `recon-course-senior` |
| Engenharia e Quality Gates | [engineering-standards.md](engineering-standards.md) | `recon-engineering.mdc` + `recon-testing.mdc` | `recon-precommit` |
| Domínio Puro (DDD) | [arquitetura.md](arquitetura.md) + [structure.md](structure.md) | `recon-domain-pure.mdc` | — |
| Arquitetura Hexagonal e Portas | [arquitetura.md](arquitetura.md) + [structure.md](structure.md) | `recon-hexagonal.mdc` | `recon-analyze-debug` |
| Observabilidade e Logging | [engineering-logging.md](engineering-logging.md) | `recon-logging.mdc` | `recon-analyze-debug` |
| Segurança em Transporte HTTP e YAML | [engineering-http-yaml-security.md](engineering-http-yaml-security.md) | `recon-http-yaml-security.mdc` | `recon-http-adapter` |
| Apresentação Terminal e Rich | [engineering-http-yaml-security.md](engineering-http-yaml-security.md) | `recon-presentation-rich.mdc` | `recon-senior-appsec` |
| Integração Contínua e Release | [engineering-ci-release.md](engineering-ci-release.md) | `recon-ci-release.mdc` | `recon-ci-release` |
| Configurações SSOT e .env | [engineering-settings-ssot.md](engineering-settings-ssot.md) | `recon-settings-ssot.mdc` | `recon-settings-change` |
| Governança de Dependências Python | [engineering-python-deps.md](engineering-python-deps.md) | `recon-python-deps.mdc` | `recon-python-deps` |
| Higienização e Limpeza do Repo | [engineering-repo-hygiene.md](engineering-repo-hygiene.md) | `recon-repo-hygiene.mdc` | `recon-repo-hygiene` |
| Sincronização de Superfícies | [engineering-surface-sync.md](engineering-surface-sync.md) | `recon-surface-sync.mdc` | `recon-surface-sync` |
| Contrato Prompt-Modelo | [prompt-model.md](../prompt-model.md) | `recon-engineering.mdc` | `recon-surface-sync` |
| Automação de Scripts e Makefile | [engineering-python.md](engineering-python.md) + [structure.md](structure.md) | `recon-scripts.mdc` | `recon-ops-runbook` |
| Interface CLI e Bootstrap | [engineering-python.md](engineering-python.md) | `recon-cli.mdc` | `recon-ops-runbook` |
| Pipeline de Análise de Aplicação | [arquitetura.md](arquitetura.md) | `recon-hexagonal.mdc` | `recon-analyze-debug` |
| Engenharia Reversa de Bundle e Swagger | [arquitetura.md](arquitetura.md) | `recon-domain-pure.mdc` | `recon-bundle-parse` |
| Auditoria e Testes de Confiabilidade | [arquitetura.md](arquitetura.md) | `recon-testing.mdc` | `recon-reliability-test` |
| Adaptador de Rede HTTP | [engineering-logging.md](engineering-logging.md) + [engineering-http-yaml-security.md](engineering-http-yaml-security.md) | `recon-hexagonal.mdc` + `recon-http-yaml-security.mdc` | `recon-http-adapter` |

---

## Mapeamento Estrutural: Camadas DDD ↔ Matriz

| Diretório no Código-Fonte | Superfície Correspondente na Matriz |
|---|---|
| `app/src/domain/` | Domínio Puro (DDD) + Engenharia Reversa de Bundle e Swagger |
| `app/src/application/ports/` | Arquitetura Hexagonal e Portas |
| `app/src/application/use_cases/` | Pipeline de Análise de Aplicação + Auditoria e Testes de Confiabilidade |
| `app/src/infrastructure/adapters/` | Adaptador de Rede HTTP |
| `app/src/infrastructure/config/` | Configurações SSOT e .env |
| `app/src/infrastructure/logging/` | Observabilidade e Logging |
| `app/src/presentation/` | Interface CLI e Bootstrap + Apresentação Terminal e Rich |
| `app/scripts/operations/` | Automação de Scripts e Makefile |
| `app/tests/` | Engenharia e Quality Gates |
| `.env.example` | Configurações SSOT e .env |

---

## Verificação Automatizada

Todas as regras em `.agents/rules/*.mdc` declaram obrigatoriamente `alwaysApply: true`.
A integridade desta matriz e a existência física de todos os artefatos mapeados são validadas de forma determinística por testes em `app/tests/unit/test_agent_coverage_matrix.py`.
