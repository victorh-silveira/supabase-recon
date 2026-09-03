# Estrutura do repositorio

## Arvore

```text
.
├── app/
│   ├── src/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── services/
│   │   │   └── validation/
│   │   ├── application/
│   │   │   ├── ports/
│   │   │   ├── use_cases/
│   │   │   └── dto/
│   │   ├── infrastructure/
│   │   │   ├── adapters/
│   │   │   ├── config/
│   │   │   └── logging/
│   │   └── presentation/
│   │       ├── cli/
│   │       └── logging/
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── domain/
│   │   │   ├── application/
│   │   │   ├── infrastructure/
│   │   │   └── presentation/
│   │   └── integration/
│   │       └── infrastructure/
│   ├── scripts/operations/
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── recon_paths.py
│   └── run.py
├── docs/
├── linters/
├── Makefile
├── AGENTS.md
├── prompt-model.md
├── README.md
├── .env.example
└── run.py
```

## Regras de dependencia

| Camada | Pode depender de |
|--------|------------------|
| domain | apenas domain |
| application | domain |
| infrastructure | application, domain |
| presentation | application, domain, infrastructure |

Ports sao contratos (`Protocol`) em `application/ports`. Adapters implementam ports em `infrastructure/adapters`.

Imports limpos (pythonpath = `app/src`):

```python
from domain.entities.asset import Asset
from application.use_cases.analyze_application import AnalyzeApplication
from infrastructure.adapters.http_client import HTTPClient
from presentation.cli.bootstrap import main
```

O gate de validate Python (`clean_workspace.py --area python --stage validate`) falha se `domain`/`application` importarem camadas externas.
