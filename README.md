# Supabase Recon Analyzer

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](app/.python-version)
[![Lint](https://img.shields.io/badge/Lint-ruff%20%7C%20isort%20%7C%20interrogate-3776AB?logo=ruff&logoColor=white)](.github/actions/lint/action.yml)
[![Tests](https://img.shields.io/badge/Tests-pytest-0F9D58?logo=pytest&logoColor=white)](app/tests/unit)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-local%20hooks%20ativos-FAB040?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
[![CI](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Quality%20%7C%20Tests%20%7C%20Security-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Release](https://img.shields.io/badge/Release-semantic--release-494949?logo=semantic-release&logoColor=white)](linters/releaserc.json)
[![API](https://img.shields.io/badge/API-PostgREST%20%7C%20Supabase-1D1E30)](https://supabase.com/docs)
[![Changelog](https://img.shields.io/badge/docs-CHANGELOG-6BA539)](docs/CHANGELOG.md)

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

O projeto segue rigorosamente os princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**:

- **Domain**: Modelos de endpoints, assets e serviços de lógica pura (Bundle Parser, Swagger Builder).
- **Application**: Casos de uso que orquestram o pipeline de análise e teste.
- **Infrastructure**: Implementações técnicas de rede (HTTP Client resiliente), loaders e persistência em disco.
- **Presentation**: Camada de entrada CLI e interface visual de alta densidade via biblioteca Rich.

---

## Configuração e Uso

### Requisitos
- Python 3.14+
- Dependências listadas em `app/requirements.txt`

### Instalação
```bash
make install
```

Ou manualmente:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r app/requirements.txt -r app/requirements-dev.txt
```

### Operação
Execute a análise completa fornecendo a URL da aplicação alvo:
```bash
make run ARGS="--url https://exemplo-lovable.app.co"
```

Ou diretamente:
```bash
python run.py --url https://exemplo-lovable.app.co
```

**Opções Adicionais:**
- `--skip-download`: Ignora o download de assets e foca apenas no parsing de código.
- `--no-test`: Desativa os testes automáticos de acessibilidade de endpoints.
- `--methods GET,POST`: Filtra quais métodos testar durante a fase de confiabilidade.

Configuração central em `config/settings.json` (timeout HTTP, diretório de saída).

---

## Qualidade e Conformidade

O projeto mantém um padrão de **Zero-Debt Policy** através de um pipeline robusto de pre-commit:

| Ferramenta | Objetivo | Métrica Exigida |
| :--- | :--- | :--- |
| **Ruff** | Linting e Formatação | Zero erros |
| **Interrogate** | Documentação de Docstrings | 100% de cobertura |
| **Pytest** | Testes Unitários | 100% de taxa de sucesso |
| **Coverage** | Cobertura de Código | 100% de linhas testadas |
| **Bandit** | Segurança Estática | Zero vulnerabilidades |
| **Pip-audit** | CVE em Dependências | Zero vulnerabilidades |

```bash
make lint
make test
make security
```

---

## Estrutura do Projeto

```text
app/
├── src/
│   ├── application        # Casos de uso (Analyze, TestReliability)
│   ├── domain             # Modelos, serviços de domínio e exceções
│   ├── infrastructure     # HTTP Client, loaders e repositório
│   └── presentation       # CLI e componentes Rich
├── scripts/               # Operações (clean_workspace, etc.)
├── tests/                 # Suíte unitária (100% coverage)
├── pyproject.toml
└── run.py                 # Entrypoint da aplicação
config/settings.json       # Configuração do repositório
linters/                   # pre-commit, commitlint, semantic-release
docs/                      # Documentação técnica
output/                    # Resultados da análise (ignorado pelo git)
run.py                     # Atalho na raiz do monorepo
```

---

## Isenção de Responsabilidade

Esta ferramenta deve ser utilizada exclusivamente para fins educacionais, de pesquisa ou em auditorias de segurança autorizadas. O uso indevido contra infraestruturas sem permissão explícita é ilegal e antiético. Os desenvolvedores não se responsabilizam por danos resultantes do uso desta ferramenta.
