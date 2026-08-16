# Dependencias Python

## Arquivos SSOT

| Arquivo | Papel |
|---------|-------|
| `app/requirements.txt` | Runtime |
| `app/requirements-dev.txt` | Lint, tipos, testes, seguranca |
| `app/pyproject.toml` | Ruff, mypy, coverage, pytest, bandit, vulture |

Nao duplicar a mesma lib em runtime e dev sem necessidade. Preferir ranges minimos coerentes com o restante do repo.

## Fluxo de mudanca

1. Justificar a dependencia (problema concreto).
2. Atualizar o requirements correto.
3. Instalar no venv WSL: `make app-install`.
4. Rodar `make app-lint` e `make app-test`.
5. Se houver CVE: `make app-security` (pip-audit); so ignore com justificativa e lista no orquestrador.

## Anti-padroes

- Adicionar framework web/DB sem port/adapter.
- Pins soltos que quebram mypy/ruff sem atualizar configs.
- Dependencia so para um script one-off (preferir stdlib ou script fora do runtime).

Rule: `recon-python-deps`. Skill: `recon-python-deps`.
