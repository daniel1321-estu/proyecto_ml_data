.PHONY: clean data lint requirements setup create_environment help

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = proyecto_ml_data
PYTHON_INTERPRETER = python

# Detect OS to set correct paths
ifeq ($(OS),Windows_NT)
    VENV_BIN := .venv/Scripts
    PYTHON := $(VENV_BIN)/python
    PIP := $(VENV_BIN)/pip
else
    VENV_BIN := .venv/bin
    PYTHON := $(VENV_BIN)/python
    PIP := $(VENV_BIN)/pip
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Setup environment and install dependencies
setup: create_environment requirements
	@echo ">>> Setup complete. Activate your environment with:"
ifeq ($(OS),Windows_NT)
	@echo "   .venv\Scripts\activate"
else
	@echo "   source .venv/bin/activate"
endif

## Create virtual environment
create_environment:
	@echo ">>> Creating virtual environment..."
	$(PYTHON_INTERPRETER) -m venv .venv

## Install Python Dependencies
requirements:
	@echo ">>> Installing dependencies from requirements.txt..."
	$(PIP) install -U pip setuptools wheel
	$(PIP) install -r requirements.txt

## Delete all compiled Python files
clean:
	@echo ">>> Cleaning python cache files..."
ifeq ($(OS),Windows_NT)
	-del /s /q *.pyc *.pyo
	-for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
else
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
endif

## Lint using flake8
lint:
	$(PIP) install flake8
	$(VENV_BIN)/flake8 src

## Run Streamlit Dashboard
dashboard:
	$(VENV_BIN)/streamlit run src/visualization/dashboard.py

.DEFAULT_GOAL := help

help:
	@echo "Available rules:"
	@echo "  setup              Create venv and install requirements"
	@echo "  create_environment Create only the .venv"
	@echo "  requirements       Install requirements in the .venv"
	@echo "  clean              Remove temporary python files"
	@echo "  lint               Check code style"
	@echo "  dashboard          Run streamlit dashboard"
