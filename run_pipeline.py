#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Orquestación del Pipeline: ETL + EDA
Este archivo permite ejecutar todo el flujo de datos desde la terminal.
"""
import os
import subprocess
import sys
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_step(command, step_name):
    """Ejecuta un comando de shell y maneja errores."""
    logger.info(f"--- Iniciando Paso: {step_name} ---")
    try:
        # Ejecutamos el comando y esperamos a que termine
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        if result.stdout:
            print(result.stdout)
        logger.info(f"✅ {step_name} completado con éxito.\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error en {step_name}:")
        print(e.stderr)
        sys.exit(1)

def get_python_executable():
    """Retorna la ruta al ejecutable de python (prioriza el entorno virtual)."""
    if os.name == 'nt': # Windows
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
    else: # Linux/Mac
        venv_python = os.path.join(".venv", "bin", "python")
    
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def main():
    # Detectar el ejecutable de python a usar
    python_exe = get_python_executable()
    logger.info(f"Usando intérprete: {python_exe}")

    # 1. Definir rutas de entrada y salida
    # Ajustamos estas rutas según la estructura del proyecto
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"
    
    # Aseguramos que los directorios existan
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # 1.5 Paso 0: Descarga de datos desde Hugging Face
    # Nota: Requiere acceso a internet
    download_cmd = f"{python_exe} src/data/download_hf_dataset.py"
    run_step(download_cmd, "Descarga de Datos (Hugging Face)")

    # 2. Paso 1: ETL (Extracción y Transformación)
    # Ejecuta src/data/make_dataset.py
    etl_cmd = f"{python_exe} src/data/make_dataset.py {RAW_DATA_DIR} {PROCESSED_DATA_DIR}"
    run_step(etl_cmd, "ETL (Procesamiento de Datos)")

    # 3. Paso 2: EDA (Análisis Exploratorio y Reportes)
    # Ejecuta src/visualization/generate_reports.py
    eda_cmd = f"{python_exe} src/visualization/generate_reports.py"
    run_step(eda_cmd, "EDA (Generación de Reportes y Gráficos)")

    logger.info("🚀 ¡Pipeline completo ejecutado con éxito!")
    logger.info("Resultados disponibles en:")
    logger.info(f"- Datos Limpios: {PROCESSED_DATA_DIR}/ventas_limpias.csv")
    logger.info("- Gráficos: reports/figures/")

if __name__ == "__main__":
    main()
