# Padrões de Observabilidade e Logging Semântico

Diretrizes para auditoria, rastreamento de eventos e mitigação de vazamento de credenciais na aplicação.

---

## 1. Princípios de Logging Estruturado

- Todos os logs emitidos pela aplicação utilizam formato semântico e estruturado.
- O subsistema é composto pela infraestrutura de logging (`app/src/infrastructure/logging/`) e adaptadores de exibição em console (`app/src/presentation/logging/`).

---

## 2. Invariantes de Segurança

1. **Mascaramento Obrigatório de Credenciais**:
   - Anon keys públicas e tokens JWT nunca devem ser impressos na íntegra em logs informativos (`INFO`).
   - O logging intercepta valores sensíveis e os mascara deterministricamente (ex.: `eyJhbGciOi...[MASCARADO]`).
2. **Proibição de Logging no Domínio**:
   - Classes e funções em `app/src/domain/` não importam nem invocam loggers.
   - O domínio retorna estados ou lança exceções especializadas; a orquestração de log ocorre nos use cases ou presentation.
3. **Controle de Volume**:
   - Proibido dump de corpos de arquivos JavaScript compilados inteiros em logs de nível padrão.
