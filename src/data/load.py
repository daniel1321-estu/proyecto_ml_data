# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def load_data(df, output_filepath):
    """
    Guarda los datos procesados en formatos CSV y Parquet.
    """
    output_dir = Path(output_filepath)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Guardar CSV
    final_csv_path = output_dir / 'ventas_limpias.csv'
    df.to_csv(final_csv_path, index=False)
    
    # Guardar Parquet
    parquet_dir = output_dir / 'store_sales_hf'
    parquet_dir.mkdir(parents=True, exist_ok=True)
    final_parquet_path = parquet_dir / 'sales_processed.parquet'
    df.to_parquet(final_parquet_path, index=False)
    
    logger.info(f'Datos guardados en: {final_csv_path} y {final_parquet_path}')
    logger.info(f'Total de registros guardados: {len(df)}')
    return final_parquet_path
