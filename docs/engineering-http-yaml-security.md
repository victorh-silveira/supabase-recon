# Segurança HTTP e YAML

Rule: `recon-http-yaml-security`. Skill: `recon-http-adapter` + `recon-senior-appsec`.

## HTTP (AS-IS)

Adapter: `infrastructure/adapters/http_client.py`.

Obrigatório:

- `requests.Session` persistente
- `HTTPAdapter` + `urllib3.Retry` (backoff; status 429/5xx)
- Timeout em toda chamada (`Settings.http_timeout_seconds`)
- Sem `verify=False`
- Falhas via `log_event`; URL com query → `?***`; sem body/payload em INFO
- Sem dump de `anon_key` em logs

Testes de integração: mock transport em `app/tests/integration`.

## YAML (AS-IS)

- Usar apenas `yaml.safe_load` (ou `CSafeLoader`)
- Proibido `yaml.load(...)` sem `SafeLoader` (risco de RCE em specs maliciosas)
- Ponto atual: `presentation/cli/bootstrap.py` ao ler `swagger.yaml`

## Rich / DTOs (AS-IS)

- Domain e application não importam `rich` nem chamam `print`/`rich.print`
- Resultados fluem como DTOs (`AnalysisReport` e correlatos) até `terminal_ui.py`

## NORTE

- Throttling explícito entre requests de reliability
- Isolamento de egress / documentação de `HTTP_PROXY`/`HTTPS_PROXY` e CA custom
- Relatórios SARIF/JSON além do terminal
