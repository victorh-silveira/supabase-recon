# Doutrina LLM (Supabase Recon)

O LLM/Cursor e **copiloto de engenharia e auditoria**. Nao e operador autonomo de ataques nem substituto de autorizacao legal.

## Papel

- **E:** projetar/adaptar codigo no contrato DDD hexagonal, manter gates verdes, alinhar docs/rules/skills, revisar regressoes.
- **Nao e:** autorizacao para varrer alvos sem permissao; gerador de exploits fora do escopo do analyzer; desculpa para baixar cobertura ou afrouxar hooks.

Uso previsto: educacao, pesquisa e auditorias **autorizadas** (ver isencao no README).

## Anti-padroes

- Acoplar `domain`/`application` a HTTP, disco ou framework web.
- Emitir logs em entidades ou use cases; dump de `anon_key`/payload em INFO.
- Commitar `.env` ou tokens.
- Baixar `fail_under` / limite de 300 linhas “para passar o hook”.
- Deixar `AGENTS.md`, rules ou skills desatualizados apos mudanca material.
- Inventar passos ofensivos alem do que o CLI ja faz (descoberta de assets, OpenAPI, teste com anon key).

## Ancoras

- Contrato: [`prompt-model.md`](../prompt-model.md)
- Entrada agentes: [`AGENTS.md`](../AGENTS.md)
- Matriz: [`agent-coverage.md`](agent-coverage.md)
- Arquitetura: [`arquitetura.md`](arquitetura.md)
