# Guia de Desenvolvimento Python e Operações

Diretrizes práticas para desenvolvimento, execução e manutenção do código em Python 3.14+.

---

## 1. Ambiente e Runtime

- **Ambiente de Desenvolvimento**: Terminal e scripts executados obrigatoriamente sob **WSL Linux**.
- **Versão do Python**: Python 3.14+.
- **Virtualenv**: Ambiente virtual recomendado em `.venv` isolado na raiz do repositório.

---

## 2. Padrões de Implementação

1. **Imports Canônicos e Futuros**:
   - Todo arquivo Python deve iniciar com:
   ```python
   from __future__ import annotations
   ```
2. **Uso de Tipagem Moderna**:
   - Utilizar sintaxe nativa de tipagem: `list[str]`, `dict[str, Any]`, `X | None` em vez de `typing.List`, `typing.Optional`.
3. **Contratos e Protocolos**:
   - Usar `typing.Protocol` para desacoplar as portas da aplicação em `app/src/application/ports/`.

---

## 3. Comandos de Desenvolvimento

- Instalar dependências: `make app-install`
- Executar testes com cobertura: `make app-test`
- Executar análise estática e validações: `make app-lint`
- Executar auditoria de segurança: `make app-security`
