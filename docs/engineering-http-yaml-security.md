# Padrões de Segurança: Transporte HTTP e Processamento YAML

Salvaguardas de segurança mandatórias contra ataques de rede, negação de serviço e desserialização arbitrária.

---

## 1. Segurança em Transporte HTTP (`HTTPClient`)

### 1.1 Mitigação contra Server-Side Request Forgery (SSRF)
- O cliente HTTP deve validar os esquemas permitidos antes de disparar requisições. Apenas `http://` e `https://` são autorizados.
- Bloqueio proativo de requisições direcionadas para:
  - Loopback (`127.0.0.1`, `localhost`, `::1`).
  - Metadados de nuvem (`169.254.169.254`, `metadata.google.internal`).
  - Faixas privadas RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) a menos que explicitamente configuradas em ambiente de testes controlados.

### 1.2 Timeouts e Retries Determinísticos
- Toda chamada externa via `requests` deve possuir timeout configurado explicitamente.
- O cliente adota backoff exponencial com limites estritos de repetições para mitigar sobrecarga em servidores remotos.

---

## 2. Processamento Seguro de Documentos YAML

- É expressamente proibido o uso de `yaml.load()` desprotegido.
- Todo processamento de arquivos ou strings YAML no projeto deve utilizar impreterivelmente `yaml.safe_load(conteudo)`.
- A geração de arquivos YAML (como especificações OpenAPI) deve utilizar `yaml.safe_dump()` garantindo sanitização de caracteres especiais.
