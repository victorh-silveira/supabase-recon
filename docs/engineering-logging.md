# Logging semantico

## API

```python
from infrastructure.logging.events import log_event

log_event(logger, logging.INFO, "recon.run.started", url=args.url)
```

## Eventos estaveis

| Evento | Quando |
|--------|--------|
| `recon.run.started` | Inicio do pipeline CLI |
| `recon.run.finished` | Sucesso |
| `recon.run.failed` | Falha de dominio ou inesperada |
| `recon.analyze.skipped_download` | Flag `--skip-download` |
| `recon.asset.download.started` | Inicio do download de assets |
| `recon.asset.download.failed` | Falha/skip de um asset |
| `recon.asset.download.finished` | Fim do download (DEBUG) |
| `recon.http.get_text.failed` | GET texto falhou |
| `recon.http.get_bytes.skipped` | GET bytes falhou |
| `recon.http.request.failed` | request generico falhou |
| `recon.file.write_text.ok` / `.failed` | Persistencia texto |
| `recon.file.write_bytes.ok` / `.failed` | Persistencia binaria |

## Regras

- Domain e use cases **nao** emitem logs.
- Caminho feliz: cerca de 3 linhas INFO (`started`, opcional `skipped_download`, `finished`).
- Sem dump de payload JSON nem body HTTP em INFO.
- URLs com query: `?***` via `redact_url`.
- Campos `anon_key` / `token` / `secret` / `password` / `authorization` viram `***`.
- `exc_info` apenas quando o logger estiver em DEBUG.
- Loggers `urllib3` e `requests` em WARNING+.
