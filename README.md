# Supabase Recon Analyzer

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)](.python-version)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%7C%20DDD-blue)](docs/arquitetura.md)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20100%25-0F9D58?logo=pytest&logoColor=white)](tests/unit)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)](.pre-commit-config.yaml)
[![Quality](https://img.shields.io/badge/Quality-Ruff-active)](pyproject.toml)
[![Documentation](https://img.shields.io/badge/Docs-Interrogate%20100%25-orange)](pyproject.toml)

Ferramenta profissional de reconhecimento e mapeamento automatizado de segurança para aplicações modernas construídas com **Lovable** e **Supabase**. O analisador realiza engenharia reversa em bundles JavaScript para descobrir infraestruturas de backend, endpoints de autenticação e tabelas expostas.

---

## 🚀 Funcionalidades

- **Descoberta Automática**: Identifica assets e o bundle principal via `sw.js` ou fallback no `index.html`.
- **Extração de Assets**: Download e organização local de todos os recursos da aplicação.
- **Mapeamento de API**:
    - **Auth**: Identificação de fluxos de login, registro e recuperação.
    - **REST**: Descoberta de tabelas e esquemas de dados expostos pelo PostgREST.
    - **RPC**: Mapeamento de funções de banco de dados e procedures.
    - **Edge Functions**: Identificação de lógica serverless em execução.
- **Swagger Generator**: Geração automática de especificação OpenAPI 3.0 completa para importação em ferramentas como Postman ou Insomnia.
- **Relatório de Confiabilidade**: Testes automatizados de acessibilidade de endpoints utilizando a `anonKey` extraída.

---

## 🏛️ Arquitetura

O projeto segue rigorosamente os princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**:

- **Domain**: Modelos de endpoints, assets e serviços de lógica pura (Bundle Parser, Swagger Builder).
- **Application**: Casos de uso que orquestram o pipeline de análise e teste.
- **Infrastructure**: Implementações técnicas de rede (HTTP Client resiliente), loaders e persistência em disco.
- **Interfaces**: Camada de entrada CLI e interface visual de alta densidade via biblioteca Rich.

---

## 🛠️ Configuração e Uso

### Requisitos
- Python 3.13+
- Dependências listadas em `requirements.txt`

### Instalação
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Operação
Execute a análise completa fornecendo a URL da aplicação alvo:
```bash
python run.py --url https://exemplo-lovable.app.co
```

**Opções Adicionais:**
- `--skip-download`: Ignora o download de assets e foca apenas no parsing de código.
- `--no-test`: Desativa os testes automáticos de acessibilidade de endpoints.
- `--methods GET,POST`: Filtra quais métodos testar durante a fase de confiabilidade.

---

## 💎 Qualidade e Conformidade

O projeto mantém um padrão de **Zero-Debt Policy** através de um pipeline robusto de pre-commit:

| Ferramenta | Objetivo | Métrica Exigida |
| :--- | :--- | :--- |
| **Ruff** | Linting e Formatação | Zero erros |
| **Interrogate** | Documentação de Docstrings | 100% de cobertura |
| **Pytest** | Testes Unitários | 100% de taxa de sucesso |
| **Coverage** | Cobertura de Código | 100% de linhas testadas |
| **Bandit** | Segurança Estática | Zero vulnerabilidades |
| **Pip-audit** | CVE em Dependências | Zero vulnerabilidades |

---

## 📁 Estrutura do Projeto

```text
src/
├── app/
│   ├── application        # Casos de Uso (Analyze, TestReliability)
│   ├── domain             # Modelos, Serviços de Domínio e Exceções
│   ├── infrastructure     # HTTP Client, Loaders e Repositório
│   └── interfaces         # CLI e Componentes Visual Rich
└── main.py                # Entrypoint principal
tests/                     # Suíte de testes unitários (100% coverage)
output/                    # Resultados da análise (Assets e Swagger YAML)
```

---

## ⚠️ Isenção de Responsabilidade

Esta ferramenta deve ser utilizada exclusivamente para fins educacionais, de pesquisa ou em auditorias de segurança autorizadas. O uso indevido contra infraestruturas sem permissão explícita é ilegal e antiético. Os desenvolvedores não se responsabilizam por danos resultantes do uso desta ferramenta.