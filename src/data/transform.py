# -*- coding: utf-8 -*-
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_data(df):
    """
    Realiza la limpieza y transformación de los datos.
    """
    logger.info('Procesando datos (Transformación)...')
    
    # Asegurar tipos
    df['date'] = pd.to_datetime(df['date'])
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    
    # Rellenar nulos básicos
    df['sales'] = df['sales'].fillna(0)
    
    logger.info('Transformación completada.')
    return df
