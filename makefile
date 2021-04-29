.PHONY: init \
init-venv \
create-venv \
update-venv \
clean \
clean-venv \
clean-pyc \
lint \
local

.DEFAULT_GOAL := help

# Python requirements
VENV ?= venv
REQUIREMENTS ?= requirements.txt
GEMFURY_TOKEN ?= $(FURY_AUTH)

# Gemfury Token Check
ifndef FURY_AUTH
$(error FURY_AUTH is not set)
endif

help:
	@echo "    init"
	@echo "        Initialize development environment."
	@echo "    init-venv"
	@echo "        Initialize Python environment."
	@echo "    create-venv"
	@echo "        Creates Python environment."
	@echo "    update-venv"
	@echo "        Update Python environment."
	@echo "    clean"
	@echo "        Remove all the development environment files."
	@echo "    clean-venv"
	@echo "        Remove Python virtual environment."
	@echo "    clean-pyc"
	@echo "        Remove Python artifacts."
	@echo "    local"
	@echo "        Run the project locally."


init: clean init-venv

init-venv: clean-venv create-venv update-venv
	@echo ""
	@echo "Do not forget to activate your new virtual environment"

create-venv:
	@echo "Creating virtual environment: $(VENV)..."
	@python3 -m venv $(VENV)

update-venv:
	@echo "Updating virtual environment: $(VENV)..."
	@( \
		. $(VENV)/bin/activate; \
		pip install --upgrade pip; \
		pip install -r $(REQUIREMENTS); \
	)


clean: clean-pyc clean-venv

clean-venv:
	@echo "Removing virtual environment: $(VENV)..."
	@rm -rf $(VENV)

clean-pyc:
	@echo "Removing compiled bytecode files..."
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-sls:
	@echo "Removing serverless files..."
	@rm -rf .serverless
	@rm -rf _warmup

clean-test: clean-pyc
	@echo "Removing previous test data..."
	@rm -rf .coverage
	@rm -rf htmlcov
	@rm -rf test-reports
	@rm -f coverage.xml
	@rm -rf .pytest_cache

lint:
	@echo "Running static type checks..."
	@( \
		. $(VENV)/bin/activate; \
		chmod +x ./bin/format.sh; \
		./bin/format.sh; \
		chmod +x ./bin/type_check.sh; \
		./bin/type_check.sh; \
	)

# Orchestation target for local deploy
local:
	@echo "Deploying to 'local'..."
	@( \
		. $(VENV)/bin/activate; \
		uvicorn app.main:app --reload; \
	)
