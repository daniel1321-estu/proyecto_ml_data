import logging
import os
from datetime import datetime

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Configura un logger que escribe en consola y, opcionalmente, en un archivo.
    """
    # 1. Crear carpeta de logs si no existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 2. Definir el formato de los logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 3. Configurar el logger principal
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicados si el logger ya tiene handlers
    if not logger.handlers:
        # Handler para Consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para Archivo (si se proporciona)
        if log_file:
            # Si no se da ruta completa, ponerlo en la carpeta logs con fecha
            if not os.path.dirname(log_file):
                log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}_{log_file}")
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
