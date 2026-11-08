# Padrões de Configuração: Single Source of Truth (SSOT)

Diretrizes para declaração, carregamento e validação de parâmetros de execução no **Supabase Recon**.

---

## 1. Princípios de Configuração

- O arquivo [`.env.example`](../.env.example) é a fonte canônica e espelho exato de todas as configurações suportadas pelo analisador.
- Todas as variáveis de configuração suportadas iniciam obrigatoriamente com o prefixo `RECON_`.
- O carregamento e tipagem são centralizados na classe `Settings` em `app/src/infrastructure/config/settings.py`.

---

## 2. Parâmetros Canônicos Suportados

| Variável | Tipo | Valor Padrão | Descrição |
|---|---|---|---|
| `RECON_APP_NAME` | `str` | `supabase-recon` | Identificador canônico da aplicação. |
| `RECON_HTTP_TIMEOUT` | `int` | `15` | Timeout padrão em segundos para requisições HTTP. |
| `RECON_HTTP_MAX_RETRIES` | `int` | `3` | Número máximo de retentativas com backoff exponencial. |
| `RECON_OUTPUT_BASE_PATH` | `Path` | `output` | Diretório base para persistência de artefatos OpenAPI e relatórios. |
| `RECON_LOG_LEVEL` | `str` | `INFO` | Nível mínimo de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `RECON_DISABLE_DOTENV` | `bool` | `false` | Se `true`, ignora o arquivo `.env` (usado em testes e CI). |

---

## 3. Invariantes de Segurança

- Proibido commitar arquivos `.env` locais no git.
- O acesso a configurações no código-fonte é feito exclusivamente injetando a instância de `Settings` a partir do bootstrap.
