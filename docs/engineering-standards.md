# Padrões de Engenharia de Software

Diretrizes mandatórias de estilo, formatação, qualidade estática e práticas de código no **Supabase Recon**.

---

## 1. Regras Inegociáveis de Código

1. **Limite Estrito de 300 Linhas**:
   - Nenhum arquivo em `app/src/**/*.py` pode ultrapassar **300 linhas** de código.
   - Violações são bloqueadas pelo hook de pre-commit e pelas esteiras de CI.
   - Refatore arquivos grandes extraindo responsabilidades e criando serviços especializados.
2. **Ausência Total de Comentários Inline**:
   - É terminantemente proibido o uso de comentários inline (`# comentário`) no código-fonte Python.
   - Toda clareza técnica deve emergir de nomes semânticos para funções/variáveis e de **docstrings completas** em módulos, classes e métodos.
3. **Tipagem Estrita**:
   - Uso obrigatório de type hints em todas as assinaturas de funções, métodos e atributos de classes.
   - Validação estrita via `mypy --strict`.

---

## 2. Linters e Formatadores

- **Formatador Oficial**: `black` com line length padrão de 88 caracteres.
- **Linter e Import Sorter**: `ruff` e `flake8` configurados em `app/pyproject.toml`.
- **Formatação de YAML e JSON**: Validados no estágio `validate` dos quality gates.

---

## 3. Pre-Commit Crash-First

O arquivo de configuração do pre-commit opera com a filosofia **crash-first**:
- Interrompe a execução imediatamente na primeira falha detectada (`fail_fast: true`).
- O estágio principal é `commit-msg`, disparando verificações essenciais antes de autorizar o commit.
