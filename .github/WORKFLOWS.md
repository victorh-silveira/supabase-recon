# GitHub Actions

CI do supabase-recon: jobs por tecnologia com steps unicos (`Python | Lint`, `Workflows | Lint`, ...). YAML/JSON no job Python. Sem Docker, Kubernetes, Terraform, deploy ou `strategy.matrix`.

## Visao (push em `main`)

```text
CI - Python
  Python | Lint
  Python | Seguranca
  Python | Testes
  Python | Validate
  Python | Build
CI - Workflows
  Workflows | Lint
        |
        v
CI - Release
  Release | Tags
  Release | Semantic
        |
        v
CI - Resumo
  Resumo | Pipeline
```

Python e Workflows em paralelo. Steps do Python sao sequenciais (crash-first). Resumo roda com `always()` apos Python, Workflows e Release.

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
├── sync-tags/
└── pipeline-summary/
```

O step `Workflows | Lint` (actionlint) analisa apenas [`.github/workflows/ci.yml`](workflows/ci.yml). O arquivo em `workflows/templates/` e markdown de anuncio, nao um workflow.

Documentacao: [docs/engineering-ci-release.md](../docs/engineering-ci-release.md).
