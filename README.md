# Sales Forecasting & Data Engineering Pipeline

Proyecto de Ingeniería de Datos y Machine Learning enfocado en el análisis histórico y la predicción de ventas para optimizar la toma de decisiones comerciales.

## 📈 Resumen del Proyecto
Este sistema implementa un pipeline completo que abarca desde la ingesta de datos crudos hasta el despliegue de modelos predictivos. El objetivo principal es identificar patrones estacionales, tendencias de mercado y el impacto de variables externas para predecir el volumen de ventas con alta precisión.

---

## 📂 Estructura del Proyecto: Guía de Carpetas

La arquitectura sigue el estándar *Cookiecutter Data Science*, diseñada para la reproducibilidad y escalabilidad:

*   **`data/`**: El corazón de los datos del proyecto.
    *   `raw/`: Datos originales e inmutables. Nunca se deben modificar.
    *   `external/`: Datos de fuentes terceras (ej. festivos, indicadores económicos).
    *   `interim/`: Datos transformados en etapas intermedias de limpieza.
    *   `processed/`: Conjuntos de datos finales y canónicos listos para el entrenamiento.
*   **`models/`**: Almacena los modelos entrenados (archivos `.pkl`, `.h5`, etc.), sus predicciones y resúmenes de rendimiento.
*   **`notebooks/`**: Cuadernos de Jupyter para Exploratory Data Analysis (EDA) y experimentación rápida. Se nombran por pasos (ej. `1.0-eda-ventas.ipynb`).
*   **`src/`**: Código fuente modular y reutilizable.
    *   `data/`: Scripts para la descarga y generación de datasets (`make_dataset.py`).
    *   `features/`: Ingeniería de variables para transformar datos crudos en features de entrenamiento (`build_features.py`).
    *   `models/`: Scripts para entrenar (`train_model.py`) y realizar inferencias (`predict_model.py`).
    *   `visualization/`: Generación de gráficos de resultados y análisis exploratorio.
*   **`reports/`**: Análisis generados en PDF/HTML y las figuras (`figures/`) utilizadas en la documentación técnica.
*   **`tests/`**: Suite de pruebas unitarias y de integración para garantizar la calidad del código y la integridad de los datos.
*   **`docs/`**: Documentación detallada del proyecto (Sphinx).
*   **`references/`**: Diccionarios de datos, manuales y materiales explicativos.

---

## 🚀 Inicio Rápido

1.  **Configuración del entorno:**
    ```bash
    make create_environment
    activate entorno
    pip install -r requirements.txt
    ```

2.  **Procesar datos y entrenar:**
    ```bash
    make data
    make train
    ```

## 🛠 Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas & NumPy** (Procesamiento)
*   **Scikit-learn / XGBoost** (Modelado)
*   **Matplotlib & Seaborn** (Visualización)
*   **Pytest** (Testing)

---
<p align="center">
  <small>Basado en el <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">Cookiecutter Data Science Template</a>.</small>
</p>
