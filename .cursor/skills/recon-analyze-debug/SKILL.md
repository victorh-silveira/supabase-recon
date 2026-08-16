---
name: recon-analyze-debug
description: >-
  Debugs the AnalyzeApplication pipeline (asset discovery, download, bundle
  parse, swagger write). Use when analysis fails, sw.js/index fallback breaks,
  swagger is missing, or the user mentions AnalyzeApplication or skip-download.
---

# Analyze debug

## Passos

1. Reproduzir CLI: `python run.py --url ...` (WSL)
2. Seguir bootstrap → `AnalyzeApplication.execute`
3. Checar discovery (`sw.js` vs `index.html`), download, `find_largest_js`
4. Validar config Supabase e paths de saida (`RECON_OUTPUT_BASE_PATH`)
5. Preferir fakes nos ports nos testes unitarios

## Docs

`docs/arquitetura.md`, rules `recon-hexagonal` + `recon-cli`
