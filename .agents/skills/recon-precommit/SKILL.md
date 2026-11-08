---
name: recon-precommit
description: >-
  Diagnóstico e correção de falhas nos hooks de pre-commit e quality gates (commitlint, linters, segurança, testes e cobertura 100%).
  Use quando commits forem bloqueados pelo pre-commit, a cobertura cair abaixo de 100% ou arquivos excederem 300 linhas.
---

# Procedimento: Diagnóstico de Pre-Commit e Quality Gates

Roteiro para resolução de bloqueios no estágio crash-first `commit-msg`.

## Ordem de Avaliação dos Gates
1. **Commitlint**:
   - Valida se o título da mensagem segue a convenção `tipo(escopo): assunto em PT-BR`.
   - Se rejeitado, ajuste a mensagem com `git commit --amend`.
2. **Lint e Validação de Formatos**:
   - Executa linters Python (`ruff`, `flake8`, `black`) e validação estrutural de arquivos YAML e JSON.
   - Corrija problemas de formatação automaticamente ou ajuste sintaxe inválida.
3. **Auditoria de Segurança**:
   - Executa `bandit` para checagem estática de código e `pip-audit` para vulnerabilidades em pacotes.
4. **Verificação Estrutural de Linhas**:
   - Nenhum arquivo em `app/src/**/*.py` pode possuir mais de 300 linhas.
   - Se violado, refatore o arquivo extraindo serviços auxiliares ou quebrando responsabilidades.
5. **Testes Unitários e Cobertura (Branch 100%)**:
   - Executa `pytest --cov=src --cov-branch --cov-fail-under=100`.
   - Toda ramificação lógica (`if`, `else`, `try/except`) deve possuir teste cobrindo o caminho.
