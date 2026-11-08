---
name: recon-ops-runbook
description: >-
  Execução operacional de tarefas e comandos do projeto via Makefile e CLI sob ambiente WSL Linux.
  Use quando configurar o ambiente local, executar análises, rodar gates de qualidade ou consultar comandos disponíveis no Makefile.
---

# Procedimento: Runbook de Operações e Execução Local

Manual de comandos operacionais para desenvolvedores e agentes sob ambiente WSL Linux.

## Comandos Principais no Makefile
```bash
# Menu interativo de ajuda com todos os comandos disponíveis
make help

# Instalação de dependências em modo de desenvolvimento
make app-install

# Execução do analisador contra uma aplicação alvo
make app-run ARGS="--url https://exemplo.lovable.app"

# Execução dos quality gates de código e configuração
make app-lint

# Auditoria de segurança estática (Bandit, pip-audit, gitleaks)
make app-security

# Execução da suíte de testes com checagem de cobertura branch 100%
make app-test

# Limpeza de caches e arquivos temporários
make app-clean

# Instalação do hook de pre-commit no git
make app-setup
```

## Execução Manual Direta do Analisador
```bash
# Análise padrão completa
python3 run.py --url https://exemplo.lovable.app

# Pular download de bundles se já baixados previamente
python3 run.py --url https://exemplo.lovable.app --skip-download

# Filtrar verbos específicos para o teste de confiabilidade
python3 run.py --url https://exemplo.lovable.app --methods GET,POST
```
