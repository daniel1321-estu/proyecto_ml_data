import pandas as pd
import os
import sys

# Configurar rutas para importar módulos locales
# El script se ejecutará desde la raíz del proyecto
sys.path.append(os.path.join(os.getcwd(), 'src'))
from visualization.visualize import plot_time_series, plot_sales_by_weekday, plot_top_families

def generate_all_reports():
    """
    Carga los datos procesados y genera todos los gráficos de análisis.
    """
    # 1. Configurar rutas
    PROCESSED_PATH = "data/processed/store_sales_hf/sales_processed.parquet"
    FIGURES_DIR = "reports/figures"
    
    if not os.path.exists(FIGURES_DIR):
        os.makedirs(FIGURES_DIR, exist_ok=True)
        print(f"Creado directorio de figuras: {FIGURES_DIR}")

    # 2. Cargar datos
    if not os.path.exists(PROCESSED_PATH):
        print(f"Error: No se encuentran los datos procesados en {PROCESSED_PATH}")
        return

    print("Cargando datos procesados...")
    df = pd.read_parquet(PROCESSED_PATH)
    df['date'] = pd.to_datetime(df['date'])

    # 3. Generar y guardar gráficos
    print("Generando gráficos de reporte...")
    
    # Gráfico 1: Serie Temporal
    plot_time_series(df, 
                     title="Tendencia Histórica de Ventas (Hugging Face Dataset)", 
                     output_path=os.path.join(FIGURES_DIR, "01_tendencia_ventas.png"))
    print("✅ Guardado: 01_tendencia_ventas.png")

    # Gráfico 2: Estacionalidad Semanal
    plot_sales_by_weekday(df, 
                          output_path=os.path.join(FIGURES_DIR, "02_estacionalidad_semanal.png"))
    print("✅ Guardado: 02_estacionalidad_semanal.png")

    # Gráfico 3: Top Categorías
    plot_top_families(df, n=15, 
                      output_path=os.path.join(FIGURES_DIR, "03_top_categorias.png"))
    print("✅ Guardado: 03_top_categorias.png")

    print("\n¡Reporte visual generado con éxito en reports/figures/!")

if __name__ == "__main__":
    generate_all_reports()
