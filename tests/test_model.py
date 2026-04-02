import unittest
import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
import sys

# Añadir src al path para importar módulos
sys.path.append(os.path.abspath("src"))

from models.train_best_model import prepare_data

class TestModel(unittest.TestCase):
    def setUp(self):
        # Crear datos de prueba pequeños
        self.sample_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'store_nbr': [1, 1],
            'family': ['BREAD/BAKERY', 'DAIRY'],
            'onpromotion': [0, 1],
            'sales': [10.5, 20.0]
        })
        self.model_path = Path("models/random_forest_model.joblib")
        self.encoder_path = Path("models/family_encoder.joblib")

    def test_prepare_data_shape(self):
        """Prueba que prepare_data devuelve X y y con las dimensiones correctas."""
        X, y, le = prepare_data(self.sample_data)
        self.assertEqual(X.shape[0], 2)
        self.assertEqual(X.shape[1], 7)  # store_nbr, family_encoded, onpromotion, year, month, day, dayofweek
        self.assertEqual(len(y), 2)

    def test_prepare_data_columns(self):
        """Prueba que prepare_data genera las columnas esperadas."""
        X, _, _ = prepare_data(self.sample_data)
        expected_cols = ['store_nbr', 'family_encoded', 'onpromotion', 'year', 'month', 'day', 'dayofweek']
        self.assertTrue(all(col in X.columns for col in expected_cols))

    def test_model_loading(self):
        """Prueba que el modelo y el encoder existen y se pueden cargar."""
        self.assertTrue(self.model_path.exists(), "El archivo del modelo no existe.")
        self.assertTrue(self.encoder_path.exists(), "El archivo del encoder no existe.")
        
        model = joblib.load(self.model_path)
        encoder = joblib.load(self.encoder_path)
        
        self.assertIsNotNone(model)
        self.assertIsNotNone(encoder)

    def test_model_prediction(self):
        """Prueba que el modelo puede realizar una predicción con datos preparados."""
        X, _, _ = prepare_data(self.sample_data)
        model = joblib.load(self.model_path)
        
        predictions = model.predict(X)
        self.assertEqual(len(predictions), 2)
        self.assertTrue(all(p >= 0 for p in predictions), "Las predicciones deben ser no negativas.")

if __name__ == '__main__':
    unittest.main()
