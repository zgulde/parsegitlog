default: help

.PHONY: pre-commit
pre-commit: fmt test check-types

.PHONY: setup
setup: ## Install development deps
	python -m pip install twine pytest isort black pytype

.PHONY: clean
clean: ## Remove built docs and packaging artifacts
	rm -rf dist build parsegitlog.egg-info public
	rm -f index.html
	rm -rf .make .mypy_cache .pytest_cache .pytype

.PHONY: release
release: fmt test check-types ## Release a new version to pypi
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

PY_FILES := $(shell find parsegitlog -name \*.py)

.PHONY: test
test: ## Run tests with pytest
	python -m pytest

.PHONY: check-types
check-types:
	python -m pytype parsegitlog

.PHONY: fmt
fmt: ## Format code with isort and black
	python -m isort --line-width 88 --trailing-comma --multi-line 3 $(PY_FILES)
	python -m black -q $(PY_FILES)

.PHONY: install-dev
install-dev: ## install with pip for development (-e)
	python -m pip install -e .

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%s\033[0m\t%s\n", $$1, $$2}' | column -ts$$'\t'
