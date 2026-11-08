---
name: recon-http-adapter
description: >-
  Manutenção e resolução de problemas no adaptador de cliente HTTP (HTTPClient), incluindo retries, timeouts, mitigação de SSRF e logging semântico.
  Use quando downloads de bundles falharem por timeout, requisições forem bloqueadas ou testes de transporte quebrarem.
---

# Procedimento: Manutenção do Cliente HTTP Resiliente

Roteiro para ajustes no adaptador de rede em `app/src/infrastructure/adapters/http_client.py`.

## Salvaguardas Mandatórias
1. **Validação de Destino (Anti-SSRF)**:
   - Validar se a URL alvo pertence a schemes seguros (`http://`, `https://`).
   - Bloquear requisições direcionadas para endereços de loopback (`127.0.0.1`, `localhost`), metadados de nuvem (`169.254.169.254`) ou redes internas RFC 1918 não autorizadas.
2. **Configuração de Timeouts**:
   - Nunca disparar `requests.get` ou `requests.post` sem timeout explícito.
   - Utilizar os valores de timeout configurados em `Settings` (`RECON_HTTP_TIMEOUT`).
3. **Estratégia de Retentativas**:
   - Configurar `urllib3.util.Retry` com backoff exponencial para códigos de status transitórios (429, 500, 502, 503, 504).
   - Limitar o número máximo de retries para evitar loops infinitos.
4. **Mocking em Testes de Unidade**:
   - Proibido realizar chamadas HTTP reais em testes unitários.
   - Utilize a fixture com `responses`, `requests_mock` ou o fake da porta `HttpClientPort`.
