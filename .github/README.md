# GitHub Actions

CI do supabase-recon: job Python (YAML/JSON validados nesse job) + Workflows (actionlint) + release semantico. Sem Docker, Kubernetes, Terraform ou deploy.

## Visao (push em `main`)

```text
CI - Python
  Python | Lint       (Ruff + YAML/JSON lint)
  Python | Seguranca
  Python | Testes
  Python | Validate   (mypy/camadas/300 + YAML/JSON validate)
  Python | Build
CI - Workflows (actionlint)
        |
        v
CI - Release (sync-tags + semantic-release)
```

Python e Workflows em paralelo. Steps do Python sao sequenciais (crash-first).

## Workflows

| Workflow | Gatilho | Uso |
|----------|---------|-----|
| [ci.yml](workflows/ci.yml) | push `main`, manual | CI + release |

## Composite actions

```text
.github/actions/ci/
├── setup-python/
├── workflows/
├── release/
└── sync-tags/
```

Orquestrador: `app/scripts/operations/clean_workspace.py --area python --stage <lint|security|test|validate|build|clean>`.

Documentacao: [docs/engineering-ci-release.md](../docs/engineering-ci-release.md).
