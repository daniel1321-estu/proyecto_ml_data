# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def extract_data(input_filepath):
    """
    Extrae los datos desde un archivo CSV.
    """
    input_file = Path(input_filepath) / 'ventas.csv'
    logger.info(f'Cargando datos desde: {input_file}')
    
    if not input_file.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_file}")
        
    df = pd.read_csv(input_file)
    logger.info(f'Total de registros extraídos: {len(df)}')
    return df

if __name__ == '__main__':
    # Esto permite ejecutarlo como script independiente si se desea
    import sys
    if len(sys.argv) > 1:
        extract_data(sys.argv[1])
