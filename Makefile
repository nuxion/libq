define USAGE
Super awesome hand-crafted build system ⚙️

Commands:
	setup     Install dependencies, dev included
	lock      Generate requirements.txt
	test      Run tests
	lint      Run linting tests
	run       Run docker image with --rm flag but mounted dirs.
	release   Publish docker image based on some variables
	docker    Build the docker image
	tag    	  Make a git tab using poetry information

endef

export USAGE
.EXPORT_ALL_VARIABLES:
GIT_TAG := $(shell git describe --tags)
BUILD := $(shell git rev-parse --short HEAD)
PROJECTNAME := $(shell basename "$(PWD)")
PACKAGE_DIR = $(shell basename "$(PWD)")
DOCKERID = $(shell echo "nuxion")

help:
	@echo "$$USAGE"

clean:
	find . ! -path "./.eggs/*" -name "*.pyc" -exec rm {} \;
	find . ! -path "./.eggs/*" -name "*.pyo" -exec rm {} \;
	find . ! -path "./.eggs/*" -name ".coverage" -exec rm {} \;
	rm -rf build/* > /dev/null 2>&1
	rm -rf dist/* > /dev/null 2>&1
	rm -rf .ipynb_checkpoints/* > /dev/null 2>&1

lock: 
	poetry export -f requirements.txt --output requirements.txt --without-hashes 


build: lock
	poetry build
	echo ${PWD}
	tar xvfz dist/${FULLPY_PKG}.tar.gz -C dist/
	cp dist/${FULLPY_PKG}/setup.py .

black:
	black --config ./.black.toml libq tests

isort:
	isort libq tests --profile=black

lint: black isort

.PHONY: test
test:
	PYTHONPATH=$(PWD) pytest --cov-report xml --cov=libq tests/

.PHONY: test-html
test-html:
	PYTHONPATH=$(PWD) pytest --cov-report=html --cov=libq tests/


.PHONY: e2e
e2e:
	pytest -s -k test_ e2e/

.PHONY: install
install:
	poetry install --dev
.PHONY: publish
publish:
	poetry publish --build

.PHONY: publish-test
publish-test:
	poetry publish --build -r test
.PHONY: docs-server
docs-serve:
	sphinx-autobuild docs docs/_build/html --port 9292 --watch ./

.PHONY: tag
tag:
	# https://git-scm.com/docs/pretty-formats/2.20.0
	#poetry version prealese
	git tag -a $(shell poetry version --short) -m "$(shell git log -1 --pretty=%s | head -n 1)"
