# Supabase Recon Analyzer

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](app/.python-version)
[![Architecture](https://img.shields.io/badge/Architecture-DDD%20%7C%20Hexagonal-0A66C2)](docs/arquitetura.md)
[![Types](https://img.shields.io/badge/mypy-strict-2A6DB0?logo=python&logoColor=white)](app/pyproject.toml)
[![Lint](https://img.shields.io/badge/Ruff-lint%20%7C%20format-D7FF64?logo=ruff&logoColor=black)](app/pyproject.toml)
[![Coverage](https://img.shields.io/badge/coverage-100%25%20branch-0F9D58)](docs/engineering-standards.md)
[![Tests](https://img.shields.io/badge/pytest-TDD%20unit%20%7C%20integration-0F9D58?logo=pytest&logoColor=white)](app/tests)
[![Security](https://img.shields.io/badge/security-bandit%20%7C%20pip--audit%20%7C%20gitleaks-C0392B)](docs/engineering-standards.md)
[![Pre-commit](https://img.shields.io/badge/pre--commit-gates%20ativos-FAB040?logo=pre-commit&logoColor=white)](linters/pre-commit-config.yaml)
[![Commits](https://img.shields.io/badge/commits-Conventional%20Commits-FE5196?logo=conventionalcommits&logoColor=white)](linters/commitlint.config.mjs)
[![CI](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml)

Ferramenta profissional de reconhecimento e mapeamento automatizado de segurança para aplicações modernas construídas com **Lovable** e **Supabase**. O analisador realiza engenharia reversa defensiva em bundles JavaScript compilados para descobrir infraestruturas de backend, endpoints de autenticação, tabelas expostas e configurações de API.

---

## Funcionalidades

- **Descoberta Automática de Assets**: Identificação de service workers (`sw.js`) com fallback determinístico para `index.html`.
- **Extração e Download Seguro de Bundles**: Download e isolamento local dos recursos compilados da aplicação.
- **Mapeamento Exaustivo de Superfície**:
  - **Auth (`/auth/v1/`)**: Fluxos de autenticação, registro e gestão de sessões.
  - **REST (`/rest/v1/`)**: Tabelas, views e operações expostas pelo PostgREST.
  - **RPC (`/rest/v1/rpc/`)**: Procedures e funções de banco de dados executáveis remotamente.
  - **Edge Functions (`/functions/v1/`)**: Funções serverless Deno/TypeScript ativas.
- **Gerador OpenAPI / Swagger**: Geração automática de especificações completas em formato OpenAPI 3.0 (YAML/JSON).
- **Auditoria de Confiabilidade (Reliability Tester)**: Testes automatizados de autorização e disponibilidade utilizando exclusivamente a chave pública `anonKey`.

---

## Arquitetura DDD Hexagonal

O projeto adota rigorosamente os padrões de **Clean Architecture** e **Domain-Driven Design (DDD)**:

- **Domain**: Entidades imutáveis, serviços puros de parsing e geração de Swagger, sem efeitos colaterais de I/O.
- **Application**: Casos de uso orquestradores e portas abstratas baseadas em `typing.Protocol`.
- **Infrastructure**: Adaptadores HTTP com mitigação contra SSRF e timeouts, persistência e logging estruturado.
- **Presentation**: Interface CLI baseada em Rich e composition root exclusivo em `presentation/cli/bootstrap.py`.

Consulte os guias detalhados:
- [Arquitetura Técnica](docs/arquitetura.md)
- [Inventário Estrutural](docs/structure.md)
- [Padrões de Engenharia](docs/engineering-standards.md)
- [Harness de Agentes de IA](AGENTS.md)
- [Matriz de Cobertura 100%](docs/agent-coverage.md)

---

## Instalação e Operação via WSL Linux

### Pré-requisitos
- Python 3.14+
- Ambiente de execução sob **WSL Linux**

### Configuração Inicial
```bash
# Menu de ajuda interativo
make help

# Configuração de ambiente e instalação de hooks
make app-setup
```

### Comandos de Execução
```bash
# Executar análise padrão completa
make app-run ARGS="--url https://exemplo.lovable.app"

# Pular download caso os bundles já existam em disco
python3 run.py --url https://exemplo.lovable.app --skip-download

# Filtrar verbos específicos para o teste de confiabilidade
python3 run.py --url https://exemplo.lovable.app --methods GET,POST
```

---

## Qualidade e Governança

```bash
# Validações estáticas de código e configuração (YAML/JSON)
make app-lint

# Auditoria de segurança (Bandit, pip-audit e gitleaks)
make app-security

# Suíte de testes com checagem obrigatória de 100% de cobertura branch
make app-test
```

---

## Harness Canônico de Inteligência Artificial

O projeto implementa o padrão canônico universal de agentes sob o diretório [`.agents/`](.agents/), acompanhado por ponte de retrocompatibilidade para o Cursor IDE em [`.cursor/`](.cursor/):
- **Regras Canônicas**: [`.agents/rules/`](.agents/rules/)
- **Habilidades Especializadas**: [`.agents/skills/`](.agents/skills/)
- **Configuração MCP**: [`.agents/mcp.json`](.agents/mcp.json)
- **Matriz de Rastreabilidade**: [`docs/agent-coverage.md`](docs/agent-coverage.md)
