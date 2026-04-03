export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "build",      // sistema de build, empacotamento ou dependências de build
        "chore",      // manutenção geral (sem impacto em código de produto)
        "ci",         // integração contínua, workflows, actions
        "docs",       // apenas documentação
        "feat",       // nova funcionalidade
        "fix",        // correção de bug
        "perf",       // melhoria de desempenho
        "qa",         // qualidade, testes manuais, gates de QA
        "refactor",   // refatoração sem mudar comportamento
        "revert",     // desfaz um commit anterior
        "style",      // formatação, whitespace, ponto e vírgula (sem lógica)
        "test",       // adicionar ou corrigir testes
      ],
    ],
    "scope-enum": [
      2,
      "always",
      [
        "all",      // alteração transversal a várias áreas
        "ci",       // GitHub Actions, pipelines
        "clean",    // limpeza de workspace, caches, housekeeping
        "config",   // ficheiros de configuração gerais
        "deps",     // dependências (requirements, package locks)
        "docs",     // pasta docs, README, CHANGELOG
        "release",  // versionamento, semantic-release, tags
        "repo",     // raiz do repositório, meta (.gitignore, templates)
        "recon",    // pacote src/recon (domínio da app)
        "script",   // um script pontual em scripts/
        "scripts",  // pasta scripts/ ou operações em lote
        "test",     // um teste ou ficheiro de teste isolado
        "tests",    // suite em tests/ ou infra de testes
        "tools",    // pasta tools/ (commitlint, releaserc, etc.)
      ],
    ],
    "scope-empty": [0],
    "subject-empty": [2, "never"],
    "type-empty": [2, "never"],
    "header-max-length": [2, "always", 100],
    "subject-case": [0],
  },
};
