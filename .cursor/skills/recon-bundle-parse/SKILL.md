---
name: recon-bundle-parse
description: >-
  Works on BundleParserService and SwaggerBuilderService (regex extraction,
  OpenAPI generation). Use when auth/REST/RPC/edge endpoints are wrong, swagger
  is incomplete, or the user mentions bundle parser or OpenAPI.
---

# Bundle / swagger

## Passos

1. Isolar fixture de bundle JS nos testes de domain
2. Ajustar regex/services **no domain** (sem HTTP)
3. Garantir `SwaggerBuilderService` cobre AUTH/REST/RPC/EDGE
4. Cobertura branch 100% nos testes de domain

## Docs

`docs/arquitetura.md`, rule `recon-domain-pure`
