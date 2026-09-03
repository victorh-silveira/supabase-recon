# Linters e qualidade

Configuracao centralizada de hooks e release semantico.

| Arquivo | Uso |
|---------|-----|
| `pre-commit-config.yaml` | `pre-commit install --config linters/pre-commit-config.yaml` |
| `commitlint.config.mjs` | Mensagens de commit (Conventional Commits) |
| `releaserc.json` | semantic-release no CI |

Os gates executam `app/scripts/operations/clean_workspace.py --area python --stage ...` (YAML/JSON no lint/validate Python). Actionlint cobre workflows no CI.
