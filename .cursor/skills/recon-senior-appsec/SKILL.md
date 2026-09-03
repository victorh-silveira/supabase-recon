---
name: recon-senior-appsec
description: >-
  Applies senior AppSec engineering checks on domain/application/adapters for
  supabase-recon. Use when changing hexagonal layers, HTTP/YAML safety, Rich
  boundaries, bundle/reliability, or the user mentions perfil senior, AppSec,
  or persona appsec-dev.
---

# Senior AppSec

## Passos

1. Ler `docs/engineering-senior-profile.md` (AS-IS vs NORTE)
2. Confirmar camadas: domain puro; ports; wiring só no bootstrap
3. HTTP/YAML: timeouts, retries, `safe_load`, sem `verify=False`, sem leak de `anon_key`
4. Rich só em presentation; DTOs a partir dos use cases
5. Se tocar bundle/swagger/reliability: skills `recon-bundle-parse` / `recon-reliability-test` / `recon-analyze-debug`
6. Testes unitários por camada + integração nos adapters; cobertura branch 100%
7. Fechar com skill `recon-surface-sync` se a mudança for material

## Docs

`docs/agents/appsec-dev.md`, `docs/engineering-http-yaml-security.md`, rules `recon-senior-profile` + `recon-http-yaml-security` + `recon-presentation-rich`
