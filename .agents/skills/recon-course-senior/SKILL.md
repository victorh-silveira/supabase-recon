---
name: recon-course-senior
description: >-
  Condução e nivelamento da trilha de capacitação sênior em AppSec e engenharia de software para o supabase-recon.
  Use quando novos engenheiros ou agentes precisarem de onboarding formal, revisão de arquitetura ou nivelamento nas diretrizes do projeto.
---

# Procedimento: Trilha de Capacitação Sênior em AppSec

Roteiro pedagógico e técnico para integração e domínio completo do repositório.

## Módulos da Trilha (`docs/courses/senior-appsec-path.md`)
1. **Módulo 1: Fundamentos e Domínio Lovable/Supabase**:
   - Como bundles de aplicações frontend expõem endpoints e anon keys públicas.
   - O papel do Supabase Recon na descoberta defensiva e mapeamento de superfície exposta.
2. **Módulo 2: Arquitetura DDD Hexagonal Estrita**:
   - Isolamento de camadas: Domain puro, Ports na Application, Adapters na Infrastructure e Bootstrap na Presentation.
   - Aplicação de `typing.Protocol` para desacoplamento de dependências.
3. **Módulo 3: Engenharia Segura e Salvaguardas**:
   - Prevenção contra SSRF, ReDoS e desserialização insegura de YAML.
   - Mascaramento e proteção de credenciais e tokens em logs.
4. **Módulo 4: Qualidade Inegociável e Quality Gates**:
   - 100% de cobertura de branches com pytest.
   - Teto inegociável de 300 linhas por arquivo.
   - Operação de pre-commit crash-first no WSL.
