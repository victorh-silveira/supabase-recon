# CI/CD e semantic-release

Rule: `recon-ci-release`. Skill: `recon-ci-release`.

## Pipeline (AS-IS)

Workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

YAML e JSON nao sao stacks: lint/validate rodam dentro do job **CI - Python**.

| Job | Conteudo |
|-----|----------|
| CI - Python | Lint (Ruff + yamllint + JSON parse), Seguranca (bandit/pip-audit/gitleaks), Testes (pytest 100%), Validate (mypy/camadas/300 + `yaml.safe_load` + JSON estrutural), Build (`compileall`) |
| CI - Workflows | `./.github/actions/ci/workflows` (actionlint) |
| CI - Release | `sync-tags` + `./.github/actions/ci/release` apos Python e Workflows |

Nao ha Docker, Kubernetes, Terraform nem workflow de CD de deploy.

`permissions: contents: read` no workflow; `contents: write` so no job de release.

Concorrencia: `cancel-in-progress: true` no grupo do workflow/ref.

Release so em `push`/`workflow_dispatch` na `main`.

Pre-commit: commitlint primeiro; depois Python | Lint, Seguranca, Testes, Validate, Build (mesmos nomes do CI).

## Semantic-release (AS-IS)

- Config: `linters/releaserc.json`
- CHANGELOG: `docs/CHANGELOG.md`
- Commit de release: `chore(release): ${version} [skip ci]`
- Install na action: pin **`conventional-changelog-conventionalcommits@9`** em `.github/actions/ci/release/action.yml`

Motivo do pin: preset `@10` exige `conventional-changelog-writer@9`; `semantic-release@25` ainda resolve writer `@8` → falha em `generateNotes`.

## Diagnostico rapido

```bash
gh run list --repo victorh-silveira/supabase-recon --limit 5
gh run view <id> --repo victorh-silveira/supabase-recon --log-failed
```

## NORTE

- Pin de `actions/checkout` (e demais) por SHA completo
- Trusted Publishing OIDC para PyPI
- Artefatos de distribuicao (wheel/binary) no GitHub Release
