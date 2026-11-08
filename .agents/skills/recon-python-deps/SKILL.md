---
name: recon-python-deps
description: >-
  Auditoria, atualização e resolução de vulnerabilidades em dependências Python (requirements.txt, requirements-dev.txt).
  Use quando adicionar/remover pacotes, resolver alertas do pip-audit ou atualizar dependências para Python 3.14+.
---

# Procedimento: Gestão de Dependências Python

Guia para manutenção e auditoria do ecossistema de dependências da aplicação.

## Padrão de Arquivos de Dependências
- `app/requirements.txt`: Dependências estritamente necessárias em tempo de execução da aplicação (ex.: `requests`, `rich`, `pydantic`).
- `app/requirements-dev.txt`: Ferramentas exclusivas de teste, lint, auditoria e tipagem (`pytest`, `mypy`, `flake8`, `bandit`, `pip-audit`).

## Fluxo de Auditoria e Atualização
1. **Executar Auditoria de Vulnerabilidades**:
   ```bash
   pip-audit -r app/requirements.txt -r app/requirements-dev.txt
   ```
2. **Atualização Segura**:
   - Caso um pacote apresente CVE conhecido, verifique a versão de correção estável.
   - Atualize a linha correspondente no manifest mantendo a pinagem (`pacote==versao`).
   - Reinstale as dependências:
   ```bash
   make app-install
   ```
3. **Verificação de Regressão**:
   - Execute a suíte de testes completa para garantir que a atualização não introduziu incompatibilidades:
   ```bash
   make app-test
   ```
