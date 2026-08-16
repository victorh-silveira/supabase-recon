# ==============================================================================
#                 SUPABASE RECON - CORE MATRIX MAKEFILE
# ==============================================================================

SHELL := /bin/bash
APP_DIR=app
PRE_COMMIT_CONFIG=linters/pre-commit-config.yaml

PYTHON := $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; elif command -v python3 >/dev/null 2>&1; then command -v python3; else echo python; fi)
PYTHON_BIN_DIR := $(dir $(PYTHON))
export PATH := $(PYTHON_BIN_DIR):$(PATH)

GREEN  := \033[1;32m
YELLOW := \033[1;33m
BLUE   := \033[1;34m
CYAN   := \033[1;36m
RED    := \033[1;31m
RESET  := \033[0m

.DEFAULT_GOAL := help

.PHONY: help app-install app-lint app-test app-security app-run app-clean \
        app-pre-commit app-pre-commit-run app-setup \
        install lint test security run pre-commit

help:
	@echo -e "$(BLUE)========================================================================$(RESET)"
	@echo -e "$(GREEN)                     SUPABASE RECON - MENU DE AJUDA                     $(RESET)"
	@echo -e "$(BLUE)========================================================================$(RESET)"
	@echo -e "Uso: $(CYAN)make <comando>$(RESET)"
	@echo -e ""
	@echo -e "$(YELLOW)Python:$(RESET) $(PYTHON)"
	@echo -e ""
	@echo -e "$(YELLOW)App:$(RESET)"
	@echo -e "  $(GREEN)app-run$(RESET)              - Executa o analyzer (ARGS=\"--url ...\")"
	@echo -e "  $(GREEN)app-install$(RESET)          - Pip (requirements + requirements-dev)"
	@echo -e "  $(GREEN)app-setup$(RESET)            - Install + hooks pre-commit/commit-msg"
	@echo -e ""
	@echo -e "$(YELLOW)Qualidade:$(RESET)"
	@echo -e "  $(GREEN)app-lint$(RESET)             - Ruff / interrogate / vulture / mypy / deps"
	@echo -e "  $(GREEN)app-test$(RESET)             - Testes + cobertura branch 100%"
	@echo -e "  $(GREEN)app-security$(RESET)         - Bandit + pip-audit"
	@echo -e "  $(GREEN)app-clean$(RESET)            - Limpa caches/artefatos locais"
	@echo -e ""
	@echo -e "$(YELLOW)Hooks:$(RESET)"
	@echo -e "  $(GREEN)app-pre-commit$(RESET)       - Instala hooks (pre-commit + commit-msg)"
	@echo -e "  $(GREEN)app-pre-commit-run$(RESET)   - Roda todos os hooks em all-files"
	@echo -e "$(BLUE)========================================================================$(RESET)"

app-install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(APP_DIR)/requirements.txt -r $(APP_DIR)/requirements-dev.txt

app-lint:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage lint

app-test:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage test

app-security:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage security

app-clean:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage clean

app-run:
	$(PYTHON) run.py $(ARGS)

app-pre-commit:
	chmod +x linters/git-hooks/bin/python linters/git-hooks/bin/resolve_venv_python.sh
	$(PYTHON) -m pre_commit install --config $(PRE_COMMIT_CONFIG)
	$(PYTHON) -m pre_commit install --hook-type commit-msg --config $(PRE_COMMIT_CONFIG)

app-pre-commit-run:
	chmod +x linters/git-hooks/bin/python linters/git-hooks/bin/resolve_venv_python.sh
	$(PYTHON) -m pre_commit run --all-files -c $(PRE_COMMIT_CONFIG)

app-setup: app-install app-pre-commit

install: app-install
lint: app-lint
test: app-test
security: app-security
run: app-run
pre-commit: app-pre-commit
