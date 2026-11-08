# Padrões de Higiene e Limpeza do Repositório

Diretrizes para prevenção de débitos técnicos, código morto e poluição da árvore git.

---

## 1. Princípios de Higiene

- Zero tolerância para arquivos temporários abandonados na raiz ou pastas da aplicação.
- Resultados de análises locais gerados em `output/` são estritamente proibidos de serem comitados.

---

## 2. Auditoria de Código Morto

- O repositório utiliza a ferramenta `vulture` para identificar símbolos, métodos, funções e classes que não são referenciados no projeto:
  ```bash
  vulture app/src/ --min-confidence 80
  ```
- Símbolos obsoletos devem ser removidos e a matriz de cobertura atualizada.

---

## 3. Limpeza Automatizada

- O comando `make app-clean` remove deterministricamente diretórios de cache (`.pytest_cache`, `__pycache__`, `.ruff_cache`) e relatórios de cobertura locais.
