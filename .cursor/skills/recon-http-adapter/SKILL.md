---
name: recon-http-adapter
description: >-
  Changes or debugs HTTPClient adapter (retries, timeouts, mock transport,
  semantic logging). Use when downloads fail, integration transport tests break,
  or the user mentions HTTPClient or requests Session.
---

# HTTP adapter

## Passos

1. Codigo em `infrastructure/adapters/http_client.py` implementando `HttpClientPort`
2. Timeout via `Settings.http_timeout_seconds`
3. Falhas: `log_event` com URL redacted; sem body em INFO
4. Integracao: mock transport em `tests/integration/infrastructure/adapters`

## Docs

`docs/engineering-logging.md`, rule `recon-hexagonal`
