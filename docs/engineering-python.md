# Engenharia Python

## Stack de qualidade

| Gate | Ferramenta |
|------|------------|
| Lint / format | Ruff |
| Types | mypy --strict |
| Dead code | vulture |
| Docstrings | interrogate (fail-under 100) |
| Test + coverage | pytest + coverage.py (branch, fail-under 100) |
| Security | bandit + pip-audit |
| Secrets (CI) | gitleaks |
| Hooks | pre-commit + commitlint |
| Release | semantic-release |

## Makefile

| Target | Acao |
|--------|------|
| `make help` | Menu de ajuda (default) |
| `make app-clean` | caches e artefatos |
| `make app-install` | Instala requirements |
| `make app-lint` | Ruff, interrogate, vulture, mypy, deps, limite 300 linhas |
| `make app-pre-commit` | instala hooks |
| `make app-pre-commit-run` | roda hooks em all-files |
| `make app-run ARGS="--url ..."` | executa o CLI |
| `make app-security` | bandit + pip-audit |
| `make app-setup` | Install + hooks pre-commit/commit-msg |
| `make app-test` | pytest + coverage branch 100% |

Orquestrador unico: `app/scripts/operations/clean_workspace.py`.
Python: `.venv/bin/python` se existir; senao `python3`/`python`.
Hooks pre-commit usam `linters/git-hooks/bin/python` (resolve o `.venv`) para nao cair no Python do sistema.

## Entrypoints

- Raiz: `python run.py --url https://...`
- App: `python app/run.py` (composition root em `presentation/cli/bootstrap.py`)

## Configuracao

Variaveis em `.env` (ver `.env.example`):

- `RECON_HTTP_TIMEOUT_SECONDS`
- `RECON_OUTPUT_BASE_PATH`
- `RECON_LOG_LEVEL`
- `RECON_DISABLE_DOTENV` (use `1` nos testes)

## Testes

- Unitarios por camada em `app/tests/unit/{domain,application,infrastructure,presentation}`
- Integracao de adapters em `app/tests/integration/infrastructure`
- Application usa fakes dos ports
- `conftest.py` define `RECON_DISABLE_DOTENV=1`

## Type checking

`mypy --strict` sobre pacotes `domain`, `application`, `infrastructure`, `presentation`.
