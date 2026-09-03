# Perfil sênior — supabase-recon

Ferramenta CLI de recon/auditoria autorizada para apps **Lovable/Supabase**.
O LLM opera como engenheiro AppSec + DevOps sênior sob [`llm-doctrine.md`](llm-doctrine.md).

Este doc separa **AS-IS** (código atual) de **NORTE** (roadmap). Não inventar AS-IS.

## Runtime e composition root (AS-IS)

- Python 3.14+, deps: `requests`, `python-dotenv`, `PyYAML`, `Rich`
- Entrypoint: `run.py` → `presentation/cli/bootstrap.py` (composition root manual)
- Bootstrap instancia adapters (`HTTPClient`, `FileRepository`, `AssetDownloader`) e injeta nos use cases
- Sem DI “mágica”; grafo sob demanda via flags CLI (`--url`, `--skip-download`, `--no-test`, `--methods`)

```text
[ CLI / bootstrap.py ]
        |
        +-- Adapters (HTTPClient, FileRepository, AssetDownloader)
        +-- Use cases (AnalyzeApplication, ApiReliabilityTester)
        +-- Presentation Rich (terminal_ui)
```

## Domínio e camadas (AS-IS)

| Conceito | Implementação atual |
|----------|---------------------|
| Bundle parse | `domain/services/bundle_parser.py` |
| OpenAPI | `domain/services/swagger_builder.py` |
| Entidades | `Asset`, `Endpoint`, `SupabaseConfig` |
| Analyze | `application/use_cases/analyze_application.py` |
| Reliability | `application/use_cases/test_api_reliability.py` |
| Ports | `HttpClientPort`, `FileRepositoryPort`, `AssetDownloaderPort` |
| UI | `presentation/cli/terminal_ui.py` + DTO `AnalysisReport` |

Domain puro: sem HTTP, filesystem, dotenv ou logging.

## HTTP / YAML / Rich (AS-IS)

- `HTTPClient`: `Session`, `HTTPAdapter` + `Retry`, timeout explícito
- YAML: `yaml.safe_load` no bootstrap; proibido `yaml.load` inseguro
- Rich só em presentation; use cases devolvem DTOs

Detalhe: [`engineering-http-yaml-security.md`](engineering-http-yaml-security.md)

## Qualidade (AS-IS)

Ruff, mypy `--strict`, vulture, interrogate 100%, pytest branch 100%, bandit, pip-audit, gitleaks (CI), pre-commit + commitlint, Make `app-*` + `clean_workspace.py`.

## CI / release (AS-IS)

Jobs paralelos quality / tests / security; release com semantic-release; preset `conventional-changelog-conventionalcommits@9`.

Detalhe: [`engineering-ci-release.md`](engineering-ci-release.md)

## NORTE (não implementar como se já existisse)

- Export SARIF/JSON estruturado além do Rich
- Packaging (pex / shiv / PyInstaller)
- Extrator AST de JS (hoje: regex no `BundleParserService`)
- Value objects `AnonKey` / `CriticalRisk` / `SecurityPosture`
- Throttling/WAF delay configurável
- pytest-xdist
- Pin de Actions por SHA completo; Trusted Publishing OIDC/PyPI
- Proxies/certs corporativos documentados além do que `requests` já herda do ambiente

## Personas e trilha

- Agentes: [`docs/agents/`](agents/)
- Curso: [`docs/courses/senior-appsec-path.md`](courses/senior-appsec-path.md)
- Skills: `recon-senior-appsec`, `recon-ci-release`, `recon-course-senior`
