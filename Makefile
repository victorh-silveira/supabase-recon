APP_DIR=app
PYTHON=python

.PHONY: install lint test security run pre-commit

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(APP_DIR)/requirements.txt -r $(APP_DIR)/requirements-dev.txt

lint:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage lint

test:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage test

security:
	$(PYTHON) $(APP_DIR)/scripts/operations/clean_workspace.py --stage security

run:
	$(PYTHON) run.py $(ARGS)

pre-commit:
	pre-commit install --config linters/pre-commit-config.yaml
