import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_processing(python_exe):
    """Ejecuta el pipeline ETL (make_dataset.py)."""
    logger.info("--- Iniciando Fase de Procesamiento (ETL) ---")
    
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"
    
    # Ejecuta src/data/make_dataset.py
    etl_cmd = f"{python_exe} src/data/make_dataset.py {RAW_DATA_DIR} {PROCESSED_DATA_DIR}"
    try:
        subprocess.run(etl_cmd, shell=True, check=True)
        logger.info("✅ Procesamiento de datos completado.\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error en el procesamiento ETL.")
        raise
