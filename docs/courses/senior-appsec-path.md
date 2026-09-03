# Curso: trilha sênior AppSec (supabase-recon)

Onboarding em módulos. Cada módulo lista doc + rule + skill. Skill condutor: `recon-course-senior`.

## Módulo 1 — Doutrina e perfil

- Ler: [`llm-doctrine.md`](../llm-doctrine.md), [`engineering-senior-profile.md`](../engineering-senior-profile.md), [`AGENTS.md`](../../AGENTS.md)
- Persona: qualquer; começar por [`agents/README.md`](../agents/README.md)
- Entrega: explicar AS-IS vs NORTE sem inventar features

## Módulo 2 — Arquitetura hexagonal

- Ler: [`arquitetura.md`](../arquitetura.md), [`structure.md`](../structure.md)
- Rules: `recon-hexagonal`, `recon-domain-pure`, `recon-cli`
- Skills: `recon-analyze-debug`, `recon-senior-appsec`
- Entrega: traçar o fluxo bootstrap → analyze → swagger → reliability

## Módulo 3 — Bundle, OpenAPI e reliability

- Skills: `recon-bundle-parse`, `recon-reliability-test`
- Doc: perfil sênior (mapa AS-IS)
- Entrega: apontar onde regex/parser e testes com anon key vivem no código

## Módulo 4 — HTTP, YAML e logging

- Docs: [`engineering-http-yaml-security.md`](../engineering-http-yaml-security.md), [`engineering-logging.md`](../engineering-logging.md)
- Rules: `recon-http-yaml-security`, `recon-logging`, `recon-presentation-rich`
- Skill: `recon-http-adapter`
- Entrega: listar proibições (`yaml.load`, `verify=False`, Rich no domain)

## Módulo 5 — Qualidade local

- Docs: [`engineering-standards.md`](../engineering-standards.md), [`engineering-python.md`](../engineering-python.md)
- Skills: `recon-ops-runbook`, `recon-precommit`
- Prática WSL: `make help`, `make app-lint`, `make app-test`, `make app-security`

## Módulo 6 — CI e release

- Doc: [`engineering-ci-release.md`](../engineering-ci-release.md)
- Rule/skill: `recon-ci-release`
- Prática: `gh run list` / `gh run view --log-failed`

## Módulo 7 — Surface sync

- Doc: [`engineering-surface-sync.md`](../engineering-surface-sync.md)
- Skill: `recon-surface-sync`
- Entrega: após mudança material, matriz `agent-coverage` coerente e gates verdes

## Critério de conclusão

Operar como as três personas em [`docs/agents/`](../agents/) sem contradizer o SSOT AS-IS.
