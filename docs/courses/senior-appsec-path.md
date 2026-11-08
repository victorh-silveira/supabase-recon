# Trilha Sênior AppSec: Do Bundle JS ao OpenAPI

Trilha estruturada de formação e nivelamento técnico para engenheiros de software e especialistas de segurança atuando no **Supabase Recon**.

---

## Módulo 1: Fundamentos do Domínio Lovable e Supabase

- **Contexto**: Como aplicações frontend compiladas em frameworks modernos expõem endpoints e anon keys de projetos Supabase.
- **Mapeamento de Superfície**:
  - `anonKey`: Chave pública para comunicação com a API Supabase.
  - REST (`/rest/v1/`): Acesso a tabelas e views via PostgREST.
  - RPC (`/rest/v1/rpc/`): Chamadas diretas a funções de banco de dados.
  - Edge Functions (`/functions/v1/`): Lógica de backend serverless em Deno/TypeScript.
  - Auth (`/auth/v1/`): Endpoints de autenticação e gestão de usuários.
- **Exercício Prático**: Inspecionar um bundle JS compilado e identificar manualmente os padrões de instanciação do cliente Supabase.

---

## Módulo 2: Arquitetura DDD Hexagonal Estrita

- **Pureza do Domínio**: Construção de entidades e serviços de parsing sem dependência de I/O ou bibliotecas de terceiros.
- **Inversão de Dependências**: Uso de `typing.Protocol` em `application/ports` para isolar use cases de implementações de rede (`requests`) ou disco.
- **Composition Root**: Centralização da montagem de dependências exclusivamente em `presentation/cli/bootstrap.py`.

---

## Módulo 3: Engenharia Segura e Mitigações

- **Prevenção contra SSRF**: Validação rigorosa de esquemas e bloqueio de endereços locais e de metadados no cliente HTTP.
- **Prevenção de ReDoS**: Análise e teste de expressões regulares de extração de bundles contra cenários de backtracking catastrófico.
- **Manipulação Segura de YAML**: Adoção de `yaml.safe_load` para prevenção de execução remota de código.
- **Mascaramento de Credenciais**: Garantia de não vazamento de segredos em logs informativos.

---

## Módulo 4: Garantia de Qualidade e Operação Canônica

- **Cobertura 100% de Branches**: Testes unitários com fakes puros cobrindo todos os caminhos lógicos.
- **Teto de 300 Linhas**: Manutenção da modularidade do código-fonte.
- **Quality Gates no WSL**: Execução unificada de verificações de lint, segurança e testes via Makefile.
