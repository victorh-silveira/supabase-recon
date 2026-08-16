---
name: recon-reliability-test
description: >-
  Debugs ApiReliabilityTester (anon key headers, method filters, path params).
  Use when endpoint reliability results look wrong, --methods filtering fails,
  or the user mentions ApiReliabilityTester or swagger test phase.
---

# Reliability test

## Passos

1. Confirmar fase nao desligada (`--no-test`)
2. Use case depende so de `HttpClientPort`
3. Headers `apikey` + `Authorization: Bearer`
4. Testes com fake HTTP; sem logs no use case

## Docs

`docs/arquitetura.md`, rule `recon-testing`
