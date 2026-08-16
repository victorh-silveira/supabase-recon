---
name: recon-settings-change
description: >-
  Changes RECON_* environment settings safely (.env.example, Settings loader,
  tests). Use when adding config knobs, changing timeouts/output/log level, or
  the user mentions .env, Settings, or RECON_DISABLE_DOTENV.
---

# Settings change

## Passos

1. Atualizar `.env.example` (sem segredos)
2. Ajustar `infrastructure/config/settings.py` e testes em `tests/unit/infrastructure/config`
3. Documentar em `docs/engineering-settings-ssot.md`
4. Garantir testes com `RECON_DISABLE_DOTENV=1`
5. Rodar gates

## Docs

`docs/engineering-settings-ssot.md`, rule `recon-settings-ssot`
