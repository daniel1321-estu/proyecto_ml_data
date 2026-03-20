import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_reporting(python_exe):
    """Ejecuta la generación de reportes y gráficos."""
    logger.info("--- Iniciando Fase de Reportes (EDA) ---")
    
    # Ejecuta src/visualization/generate_reports.py
    eda_cmd = f"{python_exe} src/visualization/generate_reports.py"
    try:
        subprocess.run(eda_cmd, shell=True, check=True)
        logger.info("✅ Reportes generados con éxito.\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error al generar reportes.")
        raise
