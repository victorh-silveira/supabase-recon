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
        |
        v
CI - Resumo (GitHub Step Summary)
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

Actionlint analisa apenas [`.github/workflows/ci.yml`](workflows/ci.yml). O arquivo em `workflows/templates/` e markdown de anuncio, nao um workflow.

Documentacao: [docs/engineering-ci-release.md](../docs/engineering-ci-release.md).
