---
name: recon-reliability-test
description: >-
  Depuração e execução do caso de uso ApiReliabilityTester (testes de autorização e disponibilidade com chave anônima).
  Use quando o teste de endpoints apresentar comportamento anômalo, a filtragem de verbos falhar ou respostas de erro forem mal interpretadas.
---

# Procedimento: Testes de Confiabilidade de Endpoints Supabase

Roteiro para diagnóstico e teste seguro de endpoints descobertos via `ApiReliabilityTester`.

## Princípios de Operação
- O teste utiliza exclusivamente a chave pública (`anonKey`) extraída do bundle da aplicação cliente.
- A finalidade é auditar se as políticas de segurança a nível de linha (Row Level Security - RLS) estão ativas e se endpoints respondem de acordo com a especificação gerada.

## Diagnóstico e Resolução
1. **Verificação de Headers Obrigatórios**:
   - As requisições enviadas pelo tester devem conter:
     - `apikey: <ANON_KEY>`
     - `Authorization: Bearer <ANON_KEY>`
2. **Filtragem de Métodos (`--methods`)**:
   - O argumento CLI aceita listas separadas por vírgula (ex.: `--methods GET,POST`).
   - Verifique se verbos não suportados ou sem payload válido são tratados de forma segura, sem causar exceções não tratadas.
3. **Mapeamento de Status HTTP**:
   - `200 OK` / `206 Partial Content`: Endpoint acessível com a chave pública anon key.
   - `401 Unauthorized` / `403 Forbidden`: Endpoint protegido por autenticação obrigatória ou RLS ativo.
   - `404 Not Found`: Endpoint ou tabela não existente no schema da API.
4. **Proteção de Logs**:
   - Certifique-se de que nenhum token JWT completo seja exposto nos logs durante a execução dos testes.
