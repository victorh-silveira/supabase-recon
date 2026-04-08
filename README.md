# supabase-recon

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](.python-version)
[![Lint](https://img.shields.io/badge/Lint-ruff%20%7C%20isort%20%7C%20interrogate-3776AB?logo=ruff&logoColor=white)](.github/actions/lint/action.yml)
[![Tests](https://img.shields.io/badge/Tests-pytest-0F9D58?logo=pytest&logoColor=white)](tests/readme.md)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-local%20hooks%20ativos-FAB040?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
[![CI](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Quality%20%7C%20Tests%20%7C%20Security-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Release](https://img.shields.io/badge/Release-semantic--release-494949?logo=semantic-release&logoColor=white)](tools/releaserc.json)
[![API](https://img.shields.io/badge/API-Supabase%20REST-1D1E30)](https://supabase.com/docs/guides/api)
[![Changelog](https://img.shields.io/badge/docs-CHANGELOG-6BA539)](docs/CHANGELOG.md)

Ferramenta de reconhecimento para aplicações Lovable/Supabase. O projeto descarrega assets públicos, localiza o bundle JS principal, extrai configuração Supabase (URL e anon key), mapeia endpoints de auth/tabelas/RPC/edge functions e gera uma especificação **OpenAPI 3** (`swagger.yaml`).

## Índice

- [Requisitos](#requisitos)
- [Arranque rápido](#arranque-rápido)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Camadas em `src/recon`](#camadas-em-srcrecon)
- [Fluxo operacional](#fluxo-operacional)
- [Saída gerada](#saída-gerada)
- [Testes e qualidade](#testes-e-qualidade)
- [CI/CD](#cicd)
- [Versões e changelog](#versões-e-changelog)
- [Uso responsável](#uso-responsável)

## Requisitos

- **Python** conforme [`.python-version`](.python-version) (3.14.x).
- Dependências de execução em [`requirements.txt`](requirements.txt).
- Dependências de desenvolvimento em [`requirements-dev.txt`](requirements-dev.txt).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Arranque rápido

```bash
python run.py --url https://exemplo.com
```

Flags principais:

- `--url` (obrigatório): URL da app alvo.
- `--skip-download`: reutiliza `output/<host>/` se já existir.
- `--no-test`: não executa a sondagem HTTP após gerar o OpenAPI.
- `--methods`: métodos na sonda (`get,post` por padrão).
- `--output-root`: muda a raiz de saída (padrão: `./output`).
- `--human-summary`: imprime resumo tabular além dos logs.

Notas:

- Se a URL vier com `http://`, o pipeline faz upgrade para `https://` automaticamente.
- Logs estruturados: `RECON_LOG_JSON=1`.
- Resumo humano por variável: `RECON_HUMAN_SUMMARY=1`.

## Estrutura do repositório

```text
.
├── .github/
│   ├── actions/                # lint, test, security, release, sync-tags
│   └── workflows/              # ci.yml
├── docs/
│   ├── CHANGELOG.md
│   └── seguranca-dependencias.md
├── scripts/
│   └── operations/
│       └── clean_workspace.py  # pipeline local de lint/docs/test/security
├── src/
│   └── recon/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       └── presentation/
├── tests/
│   ├── readme.md
│   └── unit/
├── tools/
│   ├── commitlint.config.mjs
│   └── releaserc.json
└── run.py
```

## Camadas em `src/recon`

| Camada | Papel |
|--------|-------|
| [`application`](src/recon/application/) | Orquestra o caso de uso (download, análise, OpenAPI, probe). |
| [`domain`](src/recon/domain/) | Regras puras de extração e modelagem da análise. |
| [`infrastructure`](src/recon/infrastructure/) | HTTP (`urllib`), escrita YAML e logging estruturado. |
| [`presentation`](src/recon/presentation/) | CLI e saída humana opcional. |

O bootstrap de dependências está em [`src/recon/wiring.py`](src/recon/wiring.py).

## Fluxo operacional

1. Lê `sw.js` para `precacheAndRoute`; se falhar, faz fallback para assets no `index.html`.
2. Descarrega assets e escolhe o maior `.js` como bundle principal.
3. Extrai URL Supabase, anon key, auth endpoints, tabelas, RPCs e edge functions.
4. Gera `swagger.yaml` com OpenAPI 3.
5. Opcionalmente sonda endpoints extraídos com a anon key descoberta.

## Saída gerada

Os artefatos ficam em `output/<dominio_da_app>/`:

- assets descarregados;
- `swagger.yaml` gerado;
- estrutura de diretório espelhada por rota de asset.

## Testes e qualidade

```bash
python -m pytest
python scripts/operations/clean_workspace.py --stage lint --fix-lint
python scripts/operations/clean_workspace.py --stage pytest
python scripts/operations/clean_workspace.py --stage test --coverage-fail-under 100
python scripts/operations/clean_workspace.py --stage security
pre-commit run --all-files
```

- A suíte está em [`tests/unit`](tests/unit/), organizada por camadas.
- Guia de testes em [`tests/readme.md`](tests/readme.md).
- Commits seguem Conventional Commits com regras em [`tools/commitlint.config.mjs`](tools/commitlint.config.mjs).

## CI/CD

O workflow [`ci.yml`](.github/workflows/ci.yml) dispara em `push` para `main` (com filtro por caminhos relevantes) e em `workflow_dispatch`.

Jobs de validação:

- **Qualidade**: ruff, isort, interrogate.
- **Testes**: pytest.
- **Segurança**: bandit, pip-audit, gitleaks.

O job de **Release** (semantic-release) só executa após `quality`, `tests` e `security` passarem.

## Versões e changelog

- Changelog em [`docs/CHANGELOG.md`](docs/CHANGELOG.md).
- Política de dependências e exceções de segurança em [`docs/seguranca-dependencias.md`](docs/seguranca-dependencias.md).

## Uso responsável

Utilize apenas em ambientes e aplicações para os quais tenha autorização explícita. O uso não autorizado pode violar lei e termos de serviço.

## Licença

Fornecido "como está", sem garantias. Risco por sua conta.
