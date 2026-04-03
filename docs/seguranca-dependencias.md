# Segurança das dependências Python

## PYSEC-2022-42969 (pacote `py` no PyPI)

- **Identificadores:** [PYSEC-2022-42969](https://osv.dev/vulnerability/PYSEC-2022-42969), CVE-2022-42969.
- **Pacote:** [`py`](https://pypi.org/project/py/) (dependência transitiva de ferramentas como **`interrogate`**).
- **Situação no PyPI:** a última versão publicada continua a ser **1.11.0**, no intervalo reportado. **Não existe release corrigida.**
- **Contexto:** o problema descrito (ReDoS ligado a Subversion) é **marginal** para uso típico; algumas bases **retiraram ou contestaram** o aviso. O `pip-audit` continua a reportar.

## Medidas neste repositório

1. **`interrogate`** mantém-se para **cobertura mínima de docstrings** (complementa as regras **D** do Ruff no `pyproject.toml`).
2. **`pip-audit` em `requirements.txt`:** sem ignorar vulnerabilidades.
3. **`pip-audit` em `requirements-dev.txt`:** `--ignore-vuln PYSEC-2022-42969` **apenas** para permitir a árvore que inclui `py` via `interrogate`, **documentado aqui** e replicado no `clean_workspace` e no CI (job de segurança).
4. **Não** acrescentar outros `--ignore-vuln` sem revisão e registo neste ficheiro.

## Evolução futura

- Se o `interrogate` (ou o `py`) publicar versão que deixe de ser reportada, remover o ignore correspondente do `pip-audit`.
