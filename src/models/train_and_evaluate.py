import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
import logging
import time

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_path):
    logger.info(f"Cargando datos desde {file_path}")
    df = pd.read_parquet(file_path)
    return df

def feature_engineering(df):
    logger.info("Realizando ingeniería de características...")
    df = df.copy()
    
    # Convertir fecha a características temporales
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek
    
    # Codificar la columna 'family'
    le = LabelEncoder()
    df['family_encoded'] = le.fit_transform(df['family'])
    
    # Seleccionar características y objetivo
    features = ['store_nbr', 'family_encoded', 'onpromotion', 'year', 'month', 'day', 'dayofweek']
    X = df[features]
    y = df['sales']
    
    return X, y

def evaluate_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Decision Tree": DecisionTreeRegressor(max_depth=10, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=50, max_depth=5, random_state=42)
    }
    
    results = []
    
    for name, model in models.items():
        logger.info(f"Entrenando {name}...")
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            "Model": name,
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4),
            "Training Time (s)": round(training_time, 2)
        })
        logger.info(f"Finalizado {name} en {training_time:.2f}s")
        
    return pd.DataFrame(results)

def main():
    PROCESSED_PATH = "data/processed/store_sales_hf/sales_processed.parquet"
    
    try:
        df = load_data(PROCESSED_PATH)
        
        # Para que la prueba sea rápida y no consuma toda la memoria en el CLI, usamos una muestra
        # si el dataset es muy grande. 100k registros es suficiente para una comparación inicial.
        if len(df) > 100000:
            logger.info("El dataset es grande, tomando una muestra de 100k para la comparación.")
            df = df.sample(100000, random_state=42)
            
        X, y = feature_engineering(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        results_df = evaluate_models(X_train, X_test, y_train, y_test)
        
        print("\n--- Tabla de Desempeño de Modelos ---")
        print(results_df)
        
        best_model = results_df.sort_values(by="R2", ascending=False).iloc[0]
        print(f"\n🏆 El mejor modelo es: {best_model['Model']} con un R2 de {best_model['R2']}")
        
    except Exception as e:
        logger.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
