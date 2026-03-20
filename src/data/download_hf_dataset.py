# -*- coding: utf-8 -*-
"""
Script para descargar el dataset de Hugging Face.
"""
import os
import pandas as pd
from datasets import load_dataset
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_hf_dataset():
    dataset_name = "t4tiana/store-sales-time-series-forecasting"
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    
    logger.info(f"Descargando dataset {dataset_name} desde Hugging Face...")
    try:
        # Cargamos el dataset. t4tiana/store-sales-time-series-forecasting suele tener 'train'
        dataset = load_dataset(dataset_name)
        
        # Este dataset específico suele venir con varias tablas (train, test, transactions, etc.)
        # Vamos a priorizar 'train' para el análisis de ventas
        if 'train' in dataset:
            df = dataset['train'].to_pandas()
        else:
            # Si no hay 'train', tomamos la primera partición disponible
            first_split = list(dataset.keys())[0]
            df = dataset[first_split].to_pandas()
            
        output_file = os.path.join(raw_dir, "ventas.csv")
        df.to_csv(output_file, index=False)
        
        logger.info(f"✅ Dataset real guardado con éxito en {output_file} ({len(df)} registros)")
    except Exception as e:
        logger.error(f"❌ Error descargando el dataset real: {e}")

if __name__ == "__main__":
    download_hf_dataset()
