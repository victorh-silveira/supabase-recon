# Chupabase (supabase-recon)

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
| `--human-summary` | Imprime banner e resumo em texto para além dos logs |

Logs estruturados vão para **stderr**. Para JSON por linha: `RECON_LOG_JSON=1`. Resumo humano também: `RECON_HUMAN_SUMMARY=1`.

## Saída

Ficheiros descarregados e `swagger.yaml` ficam em `output/<domínio_da_app>/` (o nome da pasta deriva do host da URL).

## Fluxo (resumo)

1. `sw.js` (`precacheAndRoute`) ou, em alternativa, assets referenciados no `index.html`
2. Descarga para disco e escolha do maior `.js` como bundle
3. Análise estática e descoberta da configuração Supabase (falha se não existir anon key no bundle)
4. Geração de `swagger.yaml` e, se não usar `--no-test`, testes opcionais aos paths listados

## Uso responsável

Utilize apenas em ambientes e aplicações para os quais tenha autorização explícita. O uso não autorizado pode violar lei e termos de serviço.

## Licença

Fornecido “como está”, sem garantias. Risco por sua conta.
