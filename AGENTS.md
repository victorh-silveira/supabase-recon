# AGENTS.md — Manifesto do Harness de IA do Supabase Recon

Ponto de entrada canônico e Single Source of Truth (SSOT) para agentes de inteligência artificial e desenvolvedores operando neste repositório.

---

## 1. Idioma e Ambiente Operacional

- **Idioma Obrigatório**: Respostas, documentações técnicas e mensagens de commit redigidas exclusivamente em **PT-BR**.
- **Ambiente de Execução**: Terminal e scripts executados obrigatoriamente sob **WSL Linux** (nunca CMD ou PowerShell nativo).
- **Sobriedade**: Proibido o uso de emojis em código-fonte, logs ou documentação técnica.
- **Autoexplicabilidade**: Proibido comentários inline no código-fonte Python (docstrings em módulos, classes e métodos são permitidas e recomendadas).

---

## 2. Universo e Domínio da Aplicação

- **Domínio**: Reconhecimento e engenharia reversa defensiva de aplicações **Lovable / Supabase**.
- **Operação**: Extração de bundles JavaScript compilados → Descoberta de `supabaseUrl`, `anonKey` e rotas REST (`/rest/v1/`), RPC (`/rpc/`), Edge Functions (`/functions/v1/`) e Auth (`/auth/v1/`) → Geração de especificação OpenAPI 3.0 → Teste de autorização e disponibilidade via chave pública anônima.
- **Arquitetura**: Domain-Driven Design (DDD) com Arquitetura Hexagonal (Ports & Adapters).
- **Configuração**: SSOT via variáveis de ambiente com prefixo `RECON_*`, `.env` e [`.env.example`](.env.example).
- **Composition Root**: Centralizado exclusivamente em `presentation/cli/bootstrap.py`.
- **Quality Gates**: Execução unificada via Makefile (`make help`, `app-lint`, `app-test`, `app-security`).

---

## 3. Doutrina do Agente: Escopo e Fronteiras Éticas

- **O que o Agente É**: Copiloto de engenharia de software sênior, auditoria defensiva de segurança e automação da qualidade do código.
- **O que o Agente NÃO É**: Uma ferramenta de ataque não autorizada. É vedada a geração de payloads ofensivos ou exploits agressivos fora do fluxo pacífico do analisador.

---

## 4. Harness Canônico e Retrocompatibilidade

- **Harness Canônico**: Diretório [`.agents/`](.agents/) contendo:
  - Regras universais: [`.agents/rules/`](.agents/rules/)
  - Habilidades especializadas: [`.agents/skills/`](.agents/skills/)
  - Manifesto MCP: [`.agents/mcp.json`](.agents/mcp.json)
- **Retrocompatibilidade com Cursor IDE**: O diretório [`.cursor/`](.cursor/) mantém symlinks relativos para `.agents/rules` e `.agents/skills`, assegurando total interoperabilidade sem duplicação física de arquivos.
- **Rastreabilidade e Matriz**: Toda a base possui 100% de cobertura mapeada em [`docs/agent-coverage.md`](docs/agent-coverage.md).

---

## 5. Proibições Globais e Invariantes

- Proibido qualquer import das camadas de `infrastructure` ou `presentation` dentro de `domain` ou `application`.
- Proibido registro de logs dentro de entidades ou casos de uso; proibido dump de tokens inteiros ou payloads brutos em nível `INFO`.
- Proibido qualquer arquivo em `app/src/**/*.py` ultrapassar o teto estrito de **300 linhas** de código.
- Proibido commits ou builds com cobertura de testes abaixo de **100% de branches**.
- Proibido versionar arquivos `.env`, tokens JWT, anon keys reais ou resultados em `output/`.
- Proibido mensagens de commit com título em outro idioma ou escopos fora da especificação do commitlint.
- Proibido afrouxar linters, suprimir checagens de segurança ou utilizar `--no-verify` para forçar commits.

---

## 6. Convenção de Commits (Conventional Commits PT-BR)

- **Formato**: `tipo(escopo): assunto descritivo em PT-BR`
- **Tipos Permitidos**: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `qa`, `refactor`, `revert`, `style`, `test`
- **Escopos Permitidos**: `all`, `app`, `bundle`, `cli`, `config`, `deps`, `domain`, `infra`, `regex`, `repo`, `swagger`, `test`, `tester`, `linters`

---

## 7. Navegação e Leitura por Tarefa

| Tipo de Tarefa | Arquivo de Leitura Inicial | Skill Recomendada |
|---|---|---|
| Qualquer alteração no repositório | este arquivo + [`docs/agent-coverage.md`](docs/agent-coverage.md) | `recon-surface-sync` |
| Núcleo de domínio, ports e segurança AppSec | [`docs/engineering-senior-profile.md`](docs/engineering-senior-profile.md) | `recon-senior-appsec` |
| Onboarding técnico e nivelamento | [`docs/courses/senior-appsec-path.md`](docs/courses/senior-appsec-path.md) | `recon-course-senior` |
| Catálogo de personas especialistas | [`docs/agents/README.md`](docs/agents/README.md) | `recon-senior-appsec` |
| Qualidade de código e pre-commit | [`docs/engineering-standards.md`](docs/engineering-standards.md) | `recon-precommit` |
| Fechamento e sincronização de superfícies | [`docs/engineering-surface-sync.md`](docs/engineering-surface-sync.md) | `recon-surface-sync` |
| Arquitetura DDD e inventário estrutural | [`docs/arquitetura.md`](docs/arquitetura.md) + [`docs/structure.md`](docs/structure.md) | `recon-analyze-debug` |
| Logging semântico e estruturado | [`docs/engineering-logging.md`](docs/engineering-logging.md) | `recon-analyze-debug` |
| Segurança em transporte HTTP e YAML | [`docs/engineering-http-yaml-security.md`](docs/engineering-http-yaml-security.md) | `recon-http-adapter` |
| CI/CD, GitHub Actions e Release | [`docs/engineering-ci-release.md`](docs/engineering-ci-release.md) | `recon-ci-release` |
| Configurações SSOT e variáveis `RECON_*` | [`docs/engineering-settings-ssot.md`](docs/engineering-settings-ssot.md) | `recon-settings-change` |
| Depuração da pipeline de análise | [`docs/arquitetura.md`](docs/arquitetura.md) | `recon-analyze-debug` |
| Engenharia reversa de bundles e OpenAPI | [`docs/arquitetura.md`](docs/arquitetura.md) | `recon-bundle-parse` |
| Testes de autorização e confiabilidade | [`docs/arquitetura.md`](docs/arquitetura.md) | `recon-reliability-test` |
| Governança de dependências Python | [`docs/engineering-python-deps.md`](docs/engineering-python-deps.md) | `recon-python-deps` |
| Higienização de código e limpeza | [`docs/engineering-repo-hygiene.md`](docs/engineering-repo-hygiene.md) | `recon-repo-hygiene` |
| Operação via Makefile e CLI | [`docs/engineering-python.md`](docs/engineering-python.md) | `recon-ops-runbook` |
