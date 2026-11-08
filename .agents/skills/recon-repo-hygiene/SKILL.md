---
name: recon-repo-hygiene
description: >-
  Higienização do repositório, identificação e remoção de código morto via vulture e expurgo de artefatos temporários órfãos.
  Use quando limpar arquivos desnecessários, auditar funções/classes não utilizadas ou preparar o repositório para releases.
---

# Procedimento: Higienização e Limpeza do Repositório

Guia de manutenção preventiva e expurgo de detritos técnicos.

## Regras de Higienização
1. **Auditoria de Código Morto**:
   - Utilize a ferramenta `vulture` para detectar funções, métodos e variáveis não referenciadas:
   ```bash
   vulture app/src/ --min-confidence 80
   ```
   - Confirme a ausência de uso real antes de remover qualquer símbolo.
2. **Expurgo de Arquivos Temporários**:
   - Remover caches de testes e compiladores:
   ```bash
   make app-clean
   ```
   - Garantir que nenhum arquivo de probe (`_tmp*`, `.log`, `.orig`) permaneça na árvore rastreada pelo git.
3. **Validação do `.gitignore`**:
   - Manter a regra `output/` ignorada para não persistir resultados de análises locais no repositório compartilhado.
