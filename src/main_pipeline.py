# -*- coding: utf-8 -*-
"""
Main Pipeline Script: Orchestrates ETL and EDA processes.
According to Cookiecutter Data Science structure.
"""
import os
import sys
import logging
import subprocess
from pathlib import Path

# Add project root and 'src' to path so we can import our modules
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

from data.extract import extract_data
from data.transform import transform_data
from data.load import load_data
from visualization.generate_reports import generate_all_reports

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_python_executable():
    """Retorna la ruta al ejecutable de python (prioriza el entorno virtual)."""
    if os.name == 'nt': # Windows
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
    else: # Linux/Mac
        venv_python = os.path.join(".venv", "bin", "python")
    
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def run_step(step_name, func, *args, **kwargs):
    """
    Ejecuta una función como un paso del pipeline y maneja el logging.
    Adaptado de run_pipeline.py para llamadas a funciones.
    """
    logger.info(f"--- Iniciando Paso: {step_name} ---")
    try:
        result = func(*args, **kwargs)
        logger.info(f"✅ {step_name} completado con éxito.\n")
        return result
    except Exception as e:
        logger.error(f"❌ Error en {step_name}: {str(e)}")
        sys.exit(1)

def run_external_step(command, step_name):
    """Ejecuta un comando de shell (para scripts externos como descarga)."""
    logger.info(f"--- Iniciando Paso Externo: {step_name} ---")
    try:
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

def main():
    # 1. Rutas
    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
    PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
    
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # 2. Paso 0: Descarga (Opcional, si existe el script)
    python_exe = get_python_executable()
    download_script = PROJECT_ROOT / "src" / "data" / "download_hf_dataset.py"
    if download_script.exists():
        download_cmd = f"{python_exe} {download_script}"
        run_external_step(download_cmd, "Descarga de Datos (Hugging Face)")
    else:
        logger.info("Paso de descarga omitido (script no encontrado).")

    # 3. Pipeline ETL (Llamando a las nuevas funciones divididas)
    df_raw = run_step("Extracción de Datos", extract_data, RAW_DATA_DIR)
    df_transformed = run_step("Transformación de Datos", transform_data, df_raw)
    run_step("Carga de Datos (Guardado)", load_data, df_transformed, PROCESSED_DATA_DIR)

    # 4. Pipeline EDA (Generación de Reportes)
    run_step("Análisis Exploratorio y Reportes", generate_all_reports)

    logger.info("🚀 ¡Pipeline completo ejecutado con éxito!")

if __name__ == "__main__":
    main()
