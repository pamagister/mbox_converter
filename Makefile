.ONESHELL:
SHELL := /bin/bash
PYTHONIOENCODING := utf-8

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	uv venv info

.PHONY: install
install:          ## Install the project in dev mode.
	$(MAKE) virtualenv
	uv pip install -e .[dev,docs]

.PHONY: lock
lock:           ## builds the uv.lock file and syncs the packages
	uv lock

.PHONY: precommit
precommit: ## Format, test and check dependencies.
	$(MAKE) fmt
	$(MAKE) test
	$(MAKE) deptry

.PHONY: fmt
fmt:              ## Format code using black & isort.
	uv run ruff format
	uv run isort mbox_converter/
	uv run black -l 100 mbox_converter/
	uv run black -l 100 tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	uv run flake8 mbox_converter/
	uv run black -l 100 --check mbox_converter/
	uv run black -l 100 --check tests/
	uv run mypy --ignore-missing-imports mbox_converter/

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	uv run pytest -v --cov-config .coveragerc --cov=mbox_converter -l --tb=short --maxfail=1 tests/
	uv run coverage xml
	uv run coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr uv run pytest -s -vvv -l --tb=long --maxfail=1 tests/

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

.PHONY: deptry
deptry:            ## Check for unused dependencies.
	uv pip install deptry
	uv run deptry .

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	uv venv

.PHONY: release
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create a version tag and push to GitHub"

	@CURRENT_VERSION=$$(cat mbox_converter/VERSION)
	IFS=. read -r MAJOR MINOR PATCH <<< "$$CURRENT_VERSION"
	@NEXT_VERSION="$$MAJOR.$$MINOR.$$((PATCH + 1))"
	@echo "Current version: $$CURRENT_VERSION"
	@read -e -i "$$NEXT_VERSION" -p "Version? (provide the next x.y.z semver) : " TAG
	@echo "$${TAG}" > mbox_converter/VERSION
	@uv run gitchangelog > HISTORY.md
	@git add mbox_converter/VERSION HISTORY.md
	@git commit -m "release: version $${TAG} 🚀"
	@echo "creating git tag : $${TAG}"
	@git tag $${TAG}
	@git push -u origin HEAD --tags
	@echo "GitHub Actions will detect the new tag and release the new version."

.PHONY: docs
docs:             ## Build and sync the documentation.
	@echo "sync documentation ..."
	@uv run ./scripts/update_readme.py
	@echo "building documentation ..."
	@uv run mkdocs build
	@uv run mkdocs serve

.PHONY: init
init:             ## Initialize the project based on an application template.
	@./.github/init.sh
