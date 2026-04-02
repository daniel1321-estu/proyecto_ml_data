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

## Compare different models (Step 1)
model-compare:
	@echo ">>> Evaluando diferentes modelos..."
	$(PYTHON) src/models/train_and_evaluate.py

## Train the best model (Random Forest) (Step 2)
model-train:
	@echo ">>> Entrenando el modelo final (Random Forest)..."
	$(PYTHON) src/models/train_best_model.py

## Run all tests (Unit and Functional)
test:
	@echo ">>> Ejecutando pruebas unitarias y funcionales..."
	$(PYTHON) -m unittest discover tests

## Run the full data pipeline (ETL + EDA)
pipeline:
	@echo ">>> Ejecutando el pipeline completo (ETL + EDA)..."
	$(PYTHON) src/main_pipeline.py

.DEFAULT_GOAL := help

help:
	@echo "Available rules:"
	@echo "  setup              Create venv and install requirements"
	@echo "  create_environment Create only the .venv"
	@echo "  requirements       Install requirements in the .venv"
	@echo "  clean              Remove temporary python files"
	@echo "  lint               Check code style"
	@echo "  dashboard          Run streamlit dashboard"
	@echo "  model-compare      Compare performance of 5 different models"
	@echo "  model-train        Train and save the best model (Random Forest)"
	@echo "  test               Run all unit and functional tests"
	@echo "  pipeline           Run the complete data pipeline (ETL + EDA)"
