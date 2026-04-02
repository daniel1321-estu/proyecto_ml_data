import unittest
import pandas as pd
import joblib
import os
import sys
from pathlib import Path

# Añadir src al path para importar módulos
sys.path.append(os.path.abspath("src"))

from data.transform import transform_data
from models.train_best_model import prepare_data

class TestFunctionalPipeline(unittest.TestCase):
    def test_end_to_end_prediction(self):
        """
        Prueba funcional completa:
        1. Carga de datos crudos (simulados).
        2. Transformación.
        3. Preparación de características.
        4. Predicción con el modelo entrenado.
        """
        # 1. Simular datos crudos
        raw_data = pd.DataFrame({
            'date': ['2023-12-01'],
            'store_nbr': [44],
            'family': ['PRODUCE'],
            'onpromotion': [10],
            'sales': [None]  # En producción, esto es lo que queremos predecir
        })
        
        # 2. Transformación de datos (usando script de limpieza)
        clean_data = transform_data(raw_data)
        self.assertIsNotNone(clean_data)
        
        # 3. Preparación para el modelo
        X, _, _ = prepare_data(clean_data)
        
        # 4. Predicción
        model_path = Path("models/random_forest_model.joblib")
        if not model_path.exists():
            self.skipTest("El modelo no ha sido entrenado, saltando prueba funcional.")
            
        model = joblib.load(model_path)
        prediction = model.predict(X)
        
        self.assertEqual(len(prediction), 1)
        print(f"Predicción funcional exitosa para Store 44, PRODUCE: {prediction[0]:.2f} ventas.")
        self.assertGreaterEqual(prediction[0], 0, "Las ventas predichas no pueden ser negativas.")

if __name__ == '__main__':
    unittest.main()
