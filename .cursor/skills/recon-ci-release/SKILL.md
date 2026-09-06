---
name: recon-ci-release
description: >-
  Diagnoses and fixes supabase-recon CI/release failures (semantic-release,
  conventionalcommits pin, gh run logs). Use when Release job fails, changelog
  generateNotes breaks, or the user mentions CI/CD, semantic-release, or
  persona release-engineer.
---

# CI / release

## Passos

1. Usar `--repo victorh-silveira/supabase-recon` no `gh` (upstream pode ser outro remoto)
2. `gh run list --limit 10` e `gh run view <id> --log-failed`
3. Se erro de changelog/writer: confirmar pin `conventional-changelog-conventionalcommits@9` em `.github/actions/ci/release/action.yml`
4. Validar `linters/releaserc.json` e Conventional Commits dos commits desde a última tag
5. Corrigir causa; nao afrouxar jobs CI (Python, Workflows, Resumo). Steps unicos `Tecnologia | Stage`, sem `strategy.matrix`
6. Após push, acompanhar `gh run watch` no novo run; conferir Step Summary do job CI - Resumo
7. Remover run falho só se o usuário pedir (`gh run delete`)

## Docs

`docs/engineering-ci-release.md`, `docs/agents/release-engineer.md`, rule `recon-ci-release`
