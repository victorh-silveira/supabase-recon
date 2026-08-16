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

Ferramenta profissional de reconhecimento e mapeamento automatizado de segurança para aplicações modernas construídas com **Lovable** e **Supabase**. O analisador realiza engenharia reversa em bundles JavaScript para descobrir infraestruturas de backend, endpoints de autenticação e tabelas expostas.

---

## Funcionalidades

- **Descoberta Automática**: Identifica assets e o bundle principal via `sw.js` ou fallback no `index.html`.
- **Extração de Assets**: Download e organização local de todos os recursos da aplicação.
- **Mapeamento de API**:
    - **Auth**: Identificação de fluxos de login, registro e recuperação.
    - **REST**: Descoberta de tabelas e esquemas de dados expostos pelo PostgREST.
    - **RPC**: Mapeamento de funções de banco de dados e procedures.
    - **Edge Functions**: Identificação de lógica serverless em execução.
- **Swagger Generator**: Geração automática de especificação OpenAPI 3.0 completa para importação em ferramentas como Postman ou Insomnia.
- **Relatório de Confiabilidade**: Testes automatizados de acessibilidade de endpoints utilizando a `anonKey` extraída.

---

## Arquitetura

O projeto segue **Clean Architecture / Hexagonal** e **DDD**:

- **Domain**: Entidades, services de parsing/swagger e validacao.
- **Application**: Use cases + ports (contratos).
- **Infrastructure**: Adapters HTTP/disco/download, Settings e logging semantico.
- **Presentation**: CLI Rich + composition root.

Detalhes: [docs/arquitetura.md](docs/arquitetura.md), [docs/structure.md](docs/structure.md), [AGENTS.md](AGENTS.md), [prompt-model.md](prompt-model.md).

Agentes Cursor: [AGENTS.md](AGENTS.md), [docs/agent-coverage.md](docs/agent-coverage.md), [`.cursor/rules`](.cursor/rules/), [`.cursor/skills`](.cursor/skills/).

---

## Configuracao e Uso

### Requisitos
- Python 3.14+
- Dependencias em `app/requirements.txt`

### Instalacao
```bash
make help
make app-setup
```

### Operacao
```bash
make app-run ARGS="--url https://exemplo-lovable.app.co"
```

Ou:
```bash
python run.py --url https://exemplo-lovable.app.co
```

Opcoes: `--skip-download`, `--no-test`, `--methods GET,POST`.

Configuracao via `.env` (ver `.env.example`): timeout HTTP, diretorio de saida, nivel de log.

---

## Qualidade e Conformidade

| Ferramenta | Objetivo | Metrica |
| :--- | :--- | :--- |
| Ruff | Lint e formatacao | Zero erros |
| mypy | Tipos estritos | --strict |
| Interrogate | Docstrings | 100% |
| Pytest + coverage | Testes (branch) | 100% |
| Bandit / pip-audit | Seguranca | Zero vulns |

```bash
make app-lint
make app-test
make app-security
make app-pre-commit-run
```

Guias: [docs/engineering-python.md](docs/engineering-python.md), [docs/engineering-logging.md](docs/engineering-logging.md).

---

## Estrutura do Projeto

```text
app/
├── src/
│   ├── domain/            # entities, services, validation
│   ├── application/       # ports, use_cases, dto
│   ├── infrastructure/    # adapters, config, logging
│   └── presentation/      # cli (composition root), logging
├── scripts/operations/    # clean_workspace (gates)
├── tests/{unit,integration}
├── pyproject.toml
└── run.py
linters/
docs/
.env.example
run.py
```

---

## Isenção de Responsabilidade

Esta ferramenta deve ser utilizada exclusivamente para fins educacionais, de pesquisa ou em auditorias de segurança autorizadas. O uso indevido contra infraestruturas sem permissão explícita é ilegal e antiético. Os desenvolvedores não se responsabilizam por danos resultantes do uso desta ferramenta.
