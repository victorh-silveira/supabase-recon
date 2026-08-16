# Settings SSOT (`.env`)

Configuracao runtime do analyzer vive em variaveis de ambiente na raiz do repositorio.

## Arquivos

| Arquivo | Papel |
|---------|-------|
| `.env` | Valores locais (nunca commitado) |
| `.env.example` | Catalogo sem segredos reais |
| `infrastructure/config/settings.py` | Loader tipado |

Testes: `RECON_DISABLE_DOTENV=1` (tambem em `app/tests/conftest.py`).

## Variaveis

| Var | Default | Papel |
|-----|---------|-------|
| `RECON_HTTP_TIMEOUT_SECONDS` | `30` | Timeout do HTTPClient |
| `RECON_OUTPUT_BASE_PATH` | `output` | Diretorio base de saida (relativo a raiz) |
| `RECON_LOG_LEVEL` | `INFO` | Nivel do root logger |
| `RECON_DISABLE_DOTENV` | `0` | `1`/`true`/`yes` pula load do `.env` |

## Fluxo de mudanca

1. Atualizar `.env.example` se a var for nova.
2. Ajustar `Settings.from_env` e testes de config.
3. Documentar aqui + rule `recon-settings-ssot`.
4. Rodar gates.

Skill: `recon-settings-change`.
