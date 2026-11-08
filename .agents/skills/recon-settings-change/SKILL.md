---
name: recon-settings-change
description: >-
  Adição ou modificação segura de variáveis de ambiente de configuração sob o prefixo RECON_ e sincronização com .env.example.
  Use quando criar novos parâmetros de timeout, caminhos de saída, níveis de log ou flags de execução.
---

# Procedimento: Alteração e Adição de Configurações SSOT

Roteiro para evolução segura do subsistema de configuração da aplicação.

## Fluxo Obrigatório de Alteração
1. **Adicionar Parâmetro em `Settings`**:
   - Editar a classe `Settings` em `app/src/infrastructure/config/settings.py`.
   - Adicionar o atributo fortemente tipado com seu respectivo prefixo `RECON_`.
2. **Atualizar `.env.example`**:
   - Incluir a nova variável no arquivo canônico `.env.example` acompanhada de comentário descritivo e valor padrão seguro.
3. **Validar Flag `RECON_DISABLE_DOTENV`**:
   - Garantir que a lógica de carregamento respeite a flag de bypass para ambientes de teste automatizado e CI.
4. **Atualizar Testes Unitários**:
   - Criar ou atualizar testes em `app/tests/unit/test_settings.py` validando os valores padrão e a sobreposição por variáveis de ambiente.
5. **Atualizar Documentação**:
   - Adicionar o novo parâmetro na tabela de referências em `docs/engineering-settings-ssot.md`.
