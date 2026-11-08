---
name: recon-bundle-parse
description: >-
  Engenharia reversa de bundles compilados via BundleParserService e geração OpenAPI via SwaggerBuilderService.
  Use quando endpoints REST, RPC, Edge Functions ou Auth não forem identificados corretamente ou a especificação OpenAPI estiver incompleta.
---

# Procedimento: Análise de Bundles e Geração OpenAPI

Roteiro para manutenção dos serviços de domínio de extração e formatação de especificações de API.

## Categorias de Endpoints Extraídos
- **REST (`/rest/v1/`)**: Tabelas e views expostas pelo PostgREST.
- **RPC (`/rest/v1/rpc/`)**: Funções de banco de dados invocáveis via PostgREST.
- **Edge Functions (`/functions/v1/`)**: Funções serverless Deno/TypeScript da aplicação.
- **Auth (`/auth/v1/`)**: Endpoints de autenticação, recuperação de credenciais e gestão de usuários.

## Verificação e Ajuste de Regex
1. **Inspeção de Padrões**:
   - Padrões residem em `app/src/domain/services/bundle_parser.py`.
   - Garantir que regex capturem variações modernas de sintaxe de clientes Supabase (`createClient`, `.from('tabela')`, `.rpc('nome')`).
2. **Prevenção de ReDoS**:
   - Expressões regulares não devem conter quantificadores aninhados que provoquem backtracking catastrófico sobre arquivos JS minificados de vários megabytes.
3. **Validação do OpenAPI**:
   - O serviço `app/src/domain/services/swagger_builder.py` gera a especificação JSON/YAML OpenAPI 3.0.
   - Validar se todos os paths identificados contêm esquemas de segurança declarando o uso de `apiKey` e `bearerAuth` via anon key.
