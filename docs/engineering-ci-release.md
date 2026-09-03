# CI/CD e semantic-release

Rule: `recon-ci-release`. Skill: `recon-ci-release`.

## Pipeline (AS-IS)

Workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

| Job | Conteúdo |
|-----|----------|
| Qualidade - Lint | action `./.github/actions/lint` |
| Testes - Pytest | action `./.github/actions/test` |
| Seguranca - Auditoria | action `./.github/actions/security` |
| Release - Versao | sync-tags + `./.github/actions/release` (após os três) |

Concorrência: `cancel-in-progress: true` no grupo do workflow/ref.

Release só em `push`/`workflow_dispatch` na `main`, com `permissions: contents: write` no job de release.

## Semantic-release (AS-IS)

- Config: `linters/releaserc.json`
- CHANGELOG: `docs/CHANGELOG.md`
- Commit de release: `chore(release): ${version} [skip ci]`
- Install na action: pin **`conventional-changelog-conventionalcommits@9`**

Motivo do pin: preset `@10` exige `conventional-changelog-writer@9`; `semantic-release@25` ainda resolve writer `@8` → falha em `generateNotes` (“Missing helper”).

## Diagnóstico rápido

```bash
gh run list --repo victorh-silveira/supabase-recon --limit 5
gh run view <id> --repo victorh-silveira/supabase-recon --log-failed
```

## NORTE

- Pin de `actions/checkout` (e demais) por SHA completo
- Jobs de auditoria com `permissions: contents: read` explícito
- Trusted Publishing OIDC para PyPI
- Artefatos de distribuição (wheel/binary) no GitHub Release
