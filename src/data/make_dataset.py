# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('--- Iniciando Pipeline ETL ---')

    # 1. Carga de datos
    input_file = Path(input_filepath) / 'ventas.csv'
    logger.info(f'Cargando datos desde: {input_file}')
    
    # Leemos solo una parte si es muy grande, o todo si la memoria lo permite.
    # El dataset tiene 3M de filas, pandas lo maneja bien en la mayoría de sistemas.
    df = pd.read_csv(input_file)

    # 2. Procesamiento (Limpieza para el dataset real de Store Sales)
    logger.info('Procesando datos reales de Store Sales...')
    
    # Asegurar tipos
    df['date'] = pd.to_datetime(df['date'])
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    
    # Rellenar nulos básicos
    df['sales'] = df['sales'].fillna(0)
    
    # Agregación diaria por familia (opcional, pero ayuda a la visualización)
    # logger.info('Agregando ventas por fecha y familia...')
    # df = df.groupby(['date', 'family']).agg({'sales': 'sum', 'onpromotion': 'sum'}).reset_index()

    # 3. Guardado de artefactos
    output_dir = Path(output_filepath)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    final_csv_path = output_dir / 'ventas_limpias.csv'
    df.to_csv(final_csv_path, index=False)
    
    parquet_dir = output_dir / 'store_sales_hf'
    parquet_dir.mkdir(parents=True, exist_ok=True)
    final_parquet_path = parquet_dir / 'sales_processed.parquet'
    df.to_parquet(final_parquet_path, index=False)
    
    logger.info(f'Pipeline finalizado. Datos guardados en: {final_csv_path} y {final_parquet_path}')
    logger.info(f'Total de registros procesados: {len(df)}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    load_dotenv(find_dotenv())
    main()
