export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "build",    // Build/Dependências externas
        "chore",    // Manutenção/Configurações de ferramentas
        "ci",       // Integração Contínua (GitHub Actions)
        "docs",     // Documentação técnica
        "feat",     // Nova funcionalidade/lógica
        "fix",      // Correção de bug no motor ou análise
        "perf",     // Melhoria de performance em download/regex
        "qa",       // Auditoria de Qualidade e Linters
        "refactor", // Refatoração de código sem mudança de lógica
        "revert",   // Reversão de commits
        "style",    // Estilo, formatação e remoção de comentários
        "test",     // Adição ou modificação de testes
      ],
    ],
    "scope-enum": [
      2,
      "always",
      [
        "all",      // Mudanças transversais ao projeto
        "app",      // Camada de Aplicação (Casos de Uso)
        "bundle",   // Lógica de análise de JS Bundles
        "cli",      // Interface de linha de comando (Presentation)
        "config",   // Alterações em arquivos de configuração
        "deps",     // Atualização de dependências (requirements)
        "domain",   // Core Domain (Entidades e Regras de Negócio)
        "infra",    // Infraestrutura (HTTP, Filesystem)
        "regex",    // Motores de extração Regex
        "repo",     // Arquivos de raiz (.gitignore, .gitattributes)
        "swagger",  // Lógica de geração do OpenAPI/YAML
        "test",     // Suite de testes unitários/integração
        "tester",   // Módulo de teste de endpoints ativos
        "tools",    // Configurações em tools/ ou hooks
      ],
    ],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "scope-empty": [0],             // Opcional
    "subject-empty": [2, "never"],
    "subject-case": [0],            // Permite Case-Sensitive para nomes de classes/métodos
    "header-max-length": [2, "always", 100],
  },
};