---
name: recon-surface-sync
description: >-
  Protocolo formal de fechamento e sincronização multidimensional de alterações (código, documentação, matriz de cobertura, regras, skills e testes).
  Use ao concluir qualquer tarefa de código, antes de submeter commits ou abrir pull requests.
---

# Procedimento: Sincronização de Superfícies (Surface Sync)

Checklist e protocolo obrigatório para garantir integridade total do repositório após qualquer modificação.

## Checklist de Encerramento de Mudança
1. **Mapeamento de Impacto**:
   - Listar todos os arquivos modificados e identificar suas respectivas superfícies em `docs/agent-coverage.md`.
2. **Atualização Documental**:
   - Se o comportamento de classes, parâmetros ou arquitetura mudou, atualizar os guias correspondentes em `docs/`.
3. **Alinhamento do Harness**:
   - Ajustar as diretrizes em `.agents/rules/*.mdc` e `.agents/skills/*/SKILL.md` se novos procedimentos foram introduzidos.
4. **Atualização da Matriz e Ponto de Entrada**:
   - Atualizar a tabela de leitura em `AGENTS.md` e a matriz de rastreabilidade em `docs/agent-coverage.md`.
5. **Higienização de Rascunhos**:
   - Remover arquivos temporários, logs locais e artefatos de testes exploratórios.
6. **Execução de Quality Gates no WSL**:
   ```bash
   make app-lint
   make app-security
   make app-test
   ```
7. **Commit Semântico Padronizado**:
   - Criar commit seguindo Conventional Commits em PT-BR:
   ```bash
   git commit -m "tipo(escopo): descricao concisa da alteracao"
   ```
