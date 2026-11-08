---
name: recon-ci-release
description: >-
  Diagnóstico e resolução de falhas nas esteiras de Integração Contínua e automação de Release (GitHub Actions, semantic-release, commitlint).
  Use quando jobs de CI falharem, notas de versão não forem geradas ou a verificação de mensagens de commit for rejeitada.
---

# Procedimento: Manutenção de CI e Release

Guia operacional para manter as esteiras de entrega contínua funcionais e seguras.

## Diagnóstico de Falhas no CI
1. **Inspeção de Logs**:
   - Utilize a CLI do GitHub ou o portal para inspecionar o job que falhou:
   ```bash
   gh run list --limit 5
   gh run view <RUN_ID> --log-failed
   ```
2. **Validação do Conventional Commits**:
   - Commits devem obedecer estritamente à configuração em `linters/commitlint.config.mjs`.
   - Formato exigido: `tipo(escopo): assunto em PT-BR`.
   - Exemplo válido: `feat(bundle): adicionar suporte a extracao de edge functions`.
3. **semantic-release**:
   - O versionamento automático dispara na branch `main`.
   - Certifique-se de que o token `GITHUB_TOKEN` possua permissões de leitura e escrita para gerar tags e releases no repositório.
