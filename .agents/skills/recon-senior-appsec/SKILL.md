---
name: recon-senior-appsec
description: >-
  Auditoria rigorosa de engenharia AppSec aplicada aos limites do DDD, clientes HTTP, segurança YAML e tratamento de anon keys.
  Use ao implementar novas rotas, modificar camadas de persistência ou auditar a segurança do analisador.
---

# Procedimento: Auditoria Sênior de Segurança da Aplicação

Checklist e critérios mandatórios para revisão de código com viés de segurança defensiva.

## Checklist de Verificação AppSec
1. **Limites Hexagonais e Injeção de Dependências**:
   - As entidades e casos de uso mantêm-se desacoplados de bibliotecas de transporte e de I/O?
   - O composition root é restrito ao bootstrap da CLI?
2. **Mitigação de Vulnerabilidades em Rede**:
   - O adaptador HTTP valida destinos contra ataques de Server-Side Request Forgery (SSRF)?
   - Os timeouts estão definidos em todas as requisições de saída?
3. **Prevenção de Execução de Código e Negação de Serviço**:
   - Todo parse de YAML utiliza exclusivamente `yaml.safe_load`?
   - As regex de parsing JS são lineares e livres de backtracking catastrófico?
4. **Proteção de Segredos e Credenciais**:
   - As anon keys extraídas são tratadas como dados sensíveis e mascaradas na camada de logging?
   - O `.env` está no `.gitignore` e não há credenciais hardcoded no repositório?
