# Inventário Estrutural do Repositório

Mapeamento exaustivo da organização de diretórios e arquivos do **Supabase Recon**.

---

## 1. Estrutura Raiz

```text
supabase-recon/
├── AGENTS.md                  # SSOT e ponto de entrada para agentes e desenvolvedores
├── .agents/                   # Harness canônico universal de IA (rules, skills, mcp.json)
├── app/                       # Código-fonte da aplicação, testes e scripts operacionais
├── docs/                      # Documentação de arquitetura, padrões e cursos
├── linters/                   # Configuração de linters, git hooks e commitlint
├── .env.example               # Modelo canônico de variáveis de ambiente suportadas
├── .gitignore                 # Regras de exclusão do git (permite !.agents/)
├── Makefile                   # Ponto focal de comandos operacionais no WSL Linux
├── prompt-model.md            # Contrato canônico de engenharia e scaffold
└── README.md                  # Apresentação do projeto e instruções de uso
```

---

## 2. Estrutura da Aplicação (`app/`)

```text
app/
├── pyproject.toml             # Configuração unificada de ferramentas (pytest, ruff, black, mypy)
├── requirements.txt           # Dependências em tempo de execução
├── requirements-dev.txt       # Dependências de teste e auditoria
├── run.py                     # Entrypoint delegado para a CLI
├── recon_paths.py             # Resolução determinística de caminhos da aplicação
├── scripts/
│   └── operations/            # Scripts de automação de qualidade e quality gates
│       ├── clean_workspace.py # Dispatcher principal de quality gates locais
│       ├── python_gates.py    # Estágios de lint, validação, segurança e testes
│       ├── config_gates.py    # Validação estrutural de arquivos YAML e JSON
│       └── gate_runtime.py    # Utilitários de execução e isolamento de runtime
├── src/
│   ├── domain/                # Camada de Domínio Puro
│   │   ├── entities/          # Modelos de dados imutáveis (Asset, Endpoint, SupabaseConfig)
│   │   ├── services/          # Serviços puros (BundleParserService, SwaggerBuilderService)
│   │   ├── validation/        # Validação pura de configurações (ConfigValidator)
│   │   └── exceptions.py      # Hierarquia de exceções de domínio
│   ├── application/           # Camada de Aplicação
│   │   ├── ports/             # Interfaces abstratas via Protocol (HTTP, FileRepo, Downloader)
│   │   └── use_cases/         # Casos de uso (AnalyzeApplication, ApiReliabilityTester)
│   ├── infrastructure/        # Camada de Infraestrutura
│   │   ├── adapters/          # Adaptadores concretos de rede e persistência
│   │   ├── config/            # Carregamento centralizado de Settings via .env
│   │   └── logging/           # Logging estruturado e mascaramento de dados
│   └── presentation/          # Camada de Apresentação
│       ├── cli/               # CLI Rich e Composition Root (bootstrap.py)
│       └── logging/           # Formatação visual de logs para o terminal
└── tests/
    ├── conftest.py            # Fixtures compartilhadas e fakes de portas
    ├── unit/                  # Testes unitários com fakes (100% de cobertura branch)
    └── integration/           # Testes de integração de adaptadores e composition root
```

---

## 3. Diretrizes de Manutenção da Estrutura

- **Limite de Linhas**: Nenhum arquivo em `app/src/**/*.py` pode exceder **300 linhas**.
- **Inversão de Dependências**: Código em `domain` ou `application` nunca importa `infrastructure` ou `presentation`.
- **Higiene**: Nenhuma pasta ou arquivo órfão deve permanecer no repositório.
