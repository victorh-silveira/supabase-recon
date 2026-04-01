# supabase-recon

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Lint](https://img.shields.io/badge/Lint-ruff%20%2B%20isort-261f3c?logo=ruff&logoColor=white)](.github/actions/lint/action.yml)
[![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)](#testes)
[![Pre-commit](https://img.shields.io/badge/Hooks-pre--commit-FAB040?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
[![CI](https://img.shields.io/github/actions/workflow/status/victorh-silveira/supabase-recon/ci.yml?branch=main&logo=github&label=CI)](https://github.com/victorh-silveira/supabase-recon/actions/workflows/ci.yml)
[![Release](https://img.shields.io/badge/Release-semantic--release-494949?logo=semantic-release&logoColor=white)](tools/releaserc.json)
[![OpenAPI](https://img.shields.io/badge/Especificação-OpenAPI%203-6BA539?logo=swagger&logoColor=white)](src/recon/domain/swagger_factory.py)

Ferramenta de reconhecimento para aplicações Lovable/Supabase: obtém assets públicos, localiza o bundle JS principal, extrai URL do projeto, chave anónima, endpoints de auth, tabelas REST, RPCs e Edge Functions, e gera um ficheiro **OpenAPI 3** (`swagger.yaml`). Opcionalmente sonda endpoints com a chave anónima descoberta.

## Requisitos

- Python 3.10+
- Dependências: `pip install -r requirements.txt` (ou também `-r requirements-dev.txt` para desenvolvimento)

## Uso

```bash
python run.py --url https://exemplo.com
```

Prefira **https://**. Se passar `http://`, o programa reescreve para **https://** automaticamente (muitos sites redirecionam e, nalgumas redes, a porta 80 falha por timeout).

Opções úteis:

| Opção | Descrição |
|-------|-----------|
| `--url` | URL da app (obrigatório) |
| `--skip-download` | Reutiliza `output/<host>/` se já existir |
| `--no-test` | Não executa sondagem HTTP após gerar o OpenAPI |
| `--methods` | Métodos na sondagem (predefinição: `get,post`) |
| `--output-root` | Pasta raiz em vez de `./output` |
| `--human-summary` | Imprime resumo em texto (tabela) para além dos logs |

Logs estruturados vão para **stderr**. Para JSON por linha: `RECON_LOG_JSON=1`. Resumo humano também: `RECON_HUMAN_SUMMARY=1`.

## Saída

Ficheiros descarregados e `swagger.yaml` ficam em `output/<domínio_da_app>/` (o nome da pasta deriva do host da URL).

## Fluxo (resumo)

1. `sw.js` (`precacheAndRoute`) ou, em alternativa, assets referenciados no `index.html`
2. Descarga para disco e escolha do maior `.js` como bundle
3. Análise estática e descoberta da configuração Supabase (falha se não existir anon key no bundle)
4. Geração de `swagger.yaml` e, se não usar `--no-test`, testes opcionais aos paths listados

## Testes

```bash
pip install -r requirements-dev.txt
python -m pytest
```

Código da suite em `tests/`.

## Histórico de versões

[docs/CHANGELOG.md](docs/CHANGELOG.md) (gerado/atualizado pelo release semântico).

## Uso responsável

Utilize apenas em ambientes e aplicações para os quais tenha autorização explícita. O uso não autorizado pode violar lei e termos de serviço.

## Licença

Fornecido “como está”, sem garantias. Risco por sua conta.
