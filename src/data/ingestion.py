import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_ingestion(python_exe):
    """Prepara directorios y descarga datos desde Hugging Face."""
    logger.info("--- Iniciando Fase de Ingesta ---")
    
    # Asegurar que existan los directorios
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Comando para descargar los datos
    download_cmd = f"{python_exe} src/data/download_hf_dataset.py"
    try:
        subprocess.run(download_cmd, shell=True, check=True)
        logger.info("✅ Ingesta de datos completada.\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error en la descarga de datos.")
        raise
