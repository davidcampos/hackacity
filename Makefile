# Help message
help:
	@echo "env: Build virtual environment for development."
	@echo "req-dev: Get development requirements."
	@echo "req-prod: Get production requirements."
	@echo "test: Run tests."
	@echo "dist: Build source and distribution wheel package."
	@echo "deploy-snapshot: Deploy snapshot to central repository."
	@echo "deploy-release: Deploy release to central repository."
	@echo "clean-build: Remove build artifacts."
	@echo "clean-pyc: Remove Python file artifacts."

# Get bin folder depending on Windows or Linux
ifeq ($(OS),Windows_NT)
    IS_WINDOWS := true
    BIN_FOLDER := env/Scripts
else
    IS_WINDOWS := false
    BIN_FOLDER := env/bin
endif

# Build virtual environment for development
env:
	virtualenv -p python3 env

# Get development requirements
req-dev:
	$(BIN_FOLDER)/pip install -r requirements/dev.txt

# Get production requirements
req-prod:
	$(BIN_FOLDER)/pip install -r requirements/prod.txt

# Run tests
test:
	$(BIN_FOLDER)/python -m unittest discover tests/

# Run tests
tox:
	$(BIN_FOLDER)/tox

# Build source and distribution wheel package
dist:
	make clean-build
	$(BIN_FOLDER)/python setup.py sdist
	$(BIN_FOLDER)/python setup.py bdist_wheel

# Deploy snapshot to central repository
deploy-snapshot:
	$(BIN_FOLDER)/python setup.py sdist bdist_wheel upload -r rb-artifactory-snapshot

# Deploy release to central repository
deploy-release:
	$(BIN_FOLDER)/python setup.py bdist_wheel upload -r rb-artifactory-release

# Remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# Remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
