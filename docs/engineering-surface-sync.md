# Protocolo de Sincronização de Superfícies (Surface Sync)

Diretrizes e checklist para garantir que toda alteração de código seja acompanhada pela atualização de suas superfícies documentais e de teste.

---

## 1. Conceito de Superfície

Uma superfície é o conjunto coeso formado por:
1. **Código-Fonte**: Arquivos de implementação (`app/src/`).
2. **Documentação de Arquitetura**: Manuais conceituais e estruturais (`docs/`).
3. **Regra Canônica de IA**: Diretriz normativa (`.agents/rules/*.mdc`).
4. **Habilidade Operacional de IA**: Procedimento acionável (`.agents/skills/*/SKILL.md`).
5. **Teste de Harness**: Validação automatizada em `app/tests/unit/test_agent_coverage_matrix.py`.

---

## 2. Checklist Obrigatório de Fechamento de Mudança

Toda alteração material deve cumprir o checklist antes do commit:
- [ ] 1. Identificar arquivos alterados e mapear suas superfícies em [`docs/agent-coverage.md`](agent-coverage.md).
- [ ] 2. Atualizar a documentação técnica relevante caso o comportamento ou contratos tenham mudado.
- [ ] 3. Alinhar as regras e skills no harness `.agents/`.
- [ ] 4. Atualizar a tabela de leitura rápida em [`AGENTS.md`](../AGENTS.md).
- [ ] 5. Executar os quality gates completos via WSL:
  ```bash
  make app-lint
  make app-security
  make app-test
  ```
- [ ] 6. Confirmar aprovação dos testes do harness:
  ```bash
  pytest app/tests/unit/test_agent_coverage_matrix.py
  ```
- [ ] 7. Gerar mensagem de commit conforme o padrão Conventional Commits em PT-BR.
