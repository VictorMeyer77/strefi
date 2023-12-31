.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: install
install:          ## Install the project in dev mode.
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	$(ENV_PREFIX)pip install -e .[test]

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort strefi/
	$(ENV_PREFIX)isort tests/
	$(ENV_PREFIX)black -l 120 strefi/
	$(ENV_PREFIX)black -l 120 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 --max-line-length 120 strefi/
	$(ENV_PREFIX)black -l 120 --check strefi/
	$(ENV_PREFIX)black -l 120 --check tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports strefi/

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=strefi -l --tb=short --maxfail=1 -p no:logging tests/
	@PYTEST_EXIT_CODE=$$?
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html
	@exit $$PYTEST_EXIT_CODE

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	@echo "creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -e .[test]
	@echo
	@echo "!!! Please run 'source .venv/bin/activate' to enable the environment !!!"

.PHONY: release
TAG := $(shell cat strefi/VERSION)
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will creates version tag and push to github"
	@git add strefi/VERSION CHANGELOG.md
	@git commit -m "release: version $(TAG) 🚀"
	@echo "creating git tag : $(TAG)"
	@git tag $(TAG)
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	@$(ENV_PREFIX)mkdocs serve