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
    logger.info(f'Cargando datos desde: {input_filepath}')
    df = pd.read_csv(Path(input_filepath) / 'ventas.csv')

    # 2. Procesamiento (Limpieza básica para demostrar en la sustentación)
    logger.info('Limpiando datos: eliminando nulos y formateando fechas...')
    
    # Rellenar categorías vacías con 'Desconocido'
    df['categoria'] = df['categoria'].fillna('Desconocido')
    
    # Eliminar filas donde falte la fecha o el precio (datos críticos)
    df = df.dropna(subset=['fecha', 'precio_unitario'])
    
    # Formatear fecha
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Añadir columna de Total (Demuestra transformación de datos)
    df['total_venta'] = df['cantidad'] * df['precio_unitario']

    # 3. Guardado de artefactos (Cumple Punto 4 de la sustentación)
    output_dir = Path(output_filepath)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    final_path = output_dir / 'ventas_limpias.csv'
    df.to_csv(final_path, index=False)
    
    logger.info(f'Pipeline finalizado. Datos guardados en: {final_path}')
    logger.info(f'Total de registros procesados: {len(df)}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
