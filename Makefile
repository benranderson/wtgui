define BROWSER_PYSCRIPT
import os, webbrowser, sys

# automatically open coverage html report results in browser
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with pylint
	pylint wtgui tests

test: ## run tests quickly with the default Python
	py.test -v

coverage: ## check code coverage quickly with the default Python
	py.test --cov-report term --cov-report html  --cov tests/ -v
	$(BROWSER) htmlcov/index.html

coverage-travis: ## check code coverage for Travis CI
	coverage run --source wtgui -m pytest tests/
	coverage report -m
	coverage html

dist: clean ## builds source and wheel package
	python setup.py sdist bdist_wheel
	ls -l dist

release: dist ## package and upload a release to PyPI
	twine upload dist/*

test-release: dist ## package and upload a release to TestPyPI
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

install: clean ## install the package to the active Python's site-packages
	python setup.py install

dinstall: clean ## install editable package to development environment
	pip install --editable .
