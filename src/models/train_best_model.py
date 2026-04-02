import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def prepare_data(df):
    logger.info("Preparando datos para el modelo final...")
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek
    
    le = LabelEncoder()
    df['family_encoded'] = le.fit_transform(df['family'])
    
    features = ['store_nbr', 'family_encoded', 'onpromotion', 'year', 'month', 'day', 'dayofweek']
    X = df[features]
    y = df['sales']
    
    return X, y, le

def train_and_save():
    PROCESSED_PATH = "data/processed/store_sales_hf/sales_processed.parquet"
    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(exist_ok=True)
    
    df = pd.read_parquet(PROCESSED_PATH)
    
    # Usamos una muestra más grande para el modelo final si es necesario, 
    # o todo el dataset si el sistema lo permite.
    if len(df) > 500000:
        logger.info("Tomando una muestra de 500k para el entrenamiento final.")
        df = df.sample(500000, random_state=42)
    
    X, y, le = prepare_data(df)
    
    logger.info("Entrenando el modelo Random Forest final...")
    model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X, y)
    
    # Guardar modelo y encoder
    joblib.dump(model, MODEL_DIR / 'random_forest_model.joblib')
    joblib.dump(le, MODEL_DIR / 'family_encoder.joblib')
    
    logger.info(f"Modelo guardado en {MODEL_DIR / 'random_forest_model.joblib'}")

if __name__ == "__main__":
    train_and_save()
