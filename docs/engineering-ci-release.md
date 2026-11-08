# Padrões de Integração Contínua (CI) e Automação de Releases

Diretrizes para esteiras do GitHub Actions, convenção de commits e versionamento semântico automatizado.

---

## 1. Fluxo de Integração Contínua (`.github/workflows/ci.yml`)

A esteira do GitHub Actions dispara em pull requests e pushes na branch `main`:
1. **Ambiente**: Execução em container Ubuntu com Python 3.14.
2. **Quality Gates**:
   - `lint`: Verificação com `ruff`, `flake8` e `black`.
   - `validate`: Validação estrutural de arquivos YAML e JSON.
   - `security`: Análise de vulnerabilidades com `bandit` e `pip-audit`.
   - `test`: Execução completa com `pytest` e validação de 100% de cobertura branch.

---

## 2. Automação de Releases com `semantic-release`

- Releases e tags de versão (`vX.Y.Z`) são geradas de forma 100% automatizada a partir do histórico de commits da branch `main`.
- A geração analisa os tipos do Conventional Commits:
  - `fix`: Dispara release de patch (`v1.0.1`).
  - `feat`: Dispara release minor (`v1.1.0`).
  - `feat!:` / `fix!:` (ou rodapé `BREAKING CHANGE`): Dispara release major (`v2.0.0`).

---

## 3. Conventional Commits em PT-BR

- Mensagens de commit fora do padrão rejeitam a esteira de CI e o hook local de pre-commit.
- Formato: `tipo(escopo): assunto conciso em PT-BR`.
