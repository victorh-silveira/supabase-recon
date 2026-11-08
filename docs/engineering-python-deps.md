# Padrões de Dependências Python e Auditoria de Segurança

Políticas de governança, gestão de dependências e prevenção contra pacotes vulneráveis.

---

## 1. Organização dos Manifestos

- `app/requirements.txt`: Dependências estritamente necessárias para a execução do analisador em produção (runtime).
- `app/requirements-dev.txt`: Ferramentas utilizadas exclusivamente durante o ciclo de desenvolvimento, linting, testes e auditoria.

---

## 2. Pinagem e Compatibilidade

- Suporte primário e canônico para **Python 3.14+**.
- Todos os pacotes declarados nos manifestos devem conter pinagem estrita de versão (ex.: `requests==2.32.3`).

---

## 3. Auditoria com `pip-audit`

- As dependências são auditadas continuamente contra bancos de dados de vulnerabilidades conhecidas (CVE/GHSA):
  ```bash
  pip-audit -r app/requirements.txt -r app/requirements-dev.txt
  ```
- Nenhuma dependência com vulnerabilidade de severidade alta ou crítica é tolerada no repositório.
