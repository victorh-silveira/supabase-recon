# Segurança das dependências Python

## PYSEC-2022-42969 (pacote `py` no PyPI)

- **Identificadores:** [PYSEC-2022-42969](https://osv.dev/vulnerability/PYSEC-2022-42969), CVE-2022-42969.
- **Pacote:** [`py`](https://pypi.org/project/py/) (utilitários históricos do ecossistema pytest).
- **Situação no PyPI:** a última versão publicada continua a ser **1.11.0**, que entra no intervalo reportado como afetado. **Não existe release corrigida** a instalar.
- **Contexto:** o problema descrito (ReDoS ligado a caminhos Subversion) é **marginal** para a maioria dos projetos; algumas bases de avisos **retiraram ou contestaram** a entrada. Mesmo assim, o `pip-audit` e ferramentas semelhantes continuam a sinalizar o pacote.

## Medidas adoptadas neste repositório

1. **Não depender de `py`:** removemos ferramentas que o puxavam como dependência transitiva (por exemplo **`interrogate`**, que dependia de `py`). Cobertura de docstrings no código fica a cargo das **regras D do Ruff** (`pyproject.toml`).
2. **`pip-audit` sem ignorar vulnerabilidades** nos ficheiros `requirements.txt` e `requirements-dev.txt` (pre-commit `clean_workspace` e job de segurança no CI).
3. **Verificação extra no CI:** após a auditoria, instala-se num **ambiente virtual novo** o conjunto `requirements.txt` + `requirements-dev.txt`. Se o pacote **`py`** aparecer na árvore, o pipeline **falha** (garantia de que nenhuma dependência declarada voltou a introduzir `py` sem revisão).

## Se precisares de uma ferramenta que ainda dependa de `py`

- Preferir **alternativas** que não usem `py`, ou abrir issue ao maintainer.
- **Não** adicionar `pip-audit --ignore-vuln` sem decisão explícita da equipa e registo neste documento (último recurso, com justificação).
