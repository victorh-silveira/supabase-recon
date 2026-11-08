---
name: recon-analyze-debug
description: >-
  Depuração e diagnóstico do pipeline completo de análise AnalyzeApplication
  (descoberta de assets, download de bundles JS, parse de metadados Supabase e escrita de OpenAPI).
  Use quando o processo de análise falhar, o fallback de sw.js/index quebrar ou artefatos não forem gerados.
---

# Procedimento: Depuração do Pipeline AnalyzeApplication

Roteiro técnico para investigar falhas na orquestração de reconhecimento de aplicações Lovable/Supabase.

## Fluxo de Execução
```text
CLI (run.py) -> Bootstrap -> AnalyzeApplication.execute()
  1. Discovery: Obter URL base e identificar assets (sw.js ou index.html)
  2. Download: Baixar bundles JavaScript para cache temporário
  3. Parsing: Identificar maior bundle JS e invocar BundleParserService
  4. Extração: Extrair supabaseUrl, anonKey e endpoints REST/RPC/Functions/Auth
  5. Escrita: Gerar especificação Swagger/OpenAPI 3.0 via SwaggerBuilderService
  6. Teste de Confiabilidade: Invocar ApiReliabilityTester (se habilitado)
```

## Passo a Passo para Diagnóstico
1. **Reproduzir o Cenário**:
   Executar a aplicação no terminal WSL Linux isolando o alvo:
   ```bash
   python3 run.py --url https://exemplo.lovable.app
   ```
2. **Inspecionar a Descoberta de Assets**:
   - Verificar se a aplicação alvo utiliza Service Worker (`/sw.js`) ou lista bundles diretamente no `/index.html`.
   - Se o Service Worker falhar, verificar o fallback automático para a página principal.
3. **Validar o Maior Bundle JS**:
   - O analisador seleciona o maior arquivo JS baixado para encontrar os endpoints. Verificar se bundles adicionais contêm rotas complementares.
4. **Validar Diretórios de Saída**:
   - Certificar que o caminho configurado em `RECON_OUTPUT_BASE_PATH` possui permissão de escrita e não está corrompido.
5. **Uso de Fakes nos Testes**:
   - Ao criar testes para cenários de erro, utilize mocks implementados nas portas (`MockHttpClient`, `InMemoryFileRepository`), sem dependência de rede externa.
