import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", title="Store Sales - Reactive Dashboard")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import os
    import sys
    from pathlib import Path
    import time
    from datetime import datetime

    # Añadimos la raíz del proyecto al path para importar nuestros módulos
    # Asumimos que el notebook se ejecuta desde la raíz o dentro de notebooks/
    PROJECT_ROOT = Path(os.getcwd()).resolve()
    if PROJECT_ROOT.name == "notebooks":
        PROJECT_ROOT = PROJECT_ROOT.parent
    
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.append(str(PROJECT_ROOT))
    
    # Intentamos importar las funciones del pipeline
    try:
        from src.data.download_hf_dataset import download_hf_dataset
        from src.main_pipeline import main as run_full_pipeline
        pipeline_available = True
    except ImportError:
        pipeline_available = False

    return (
        PROJECT_ROOT,
        datetime,
        download_hf_dataset,
        mo,
        os,
        pd,
        pipeline_available,
        px,
        run_full_pipeline,
        sys,
        time,
    )


@app.cell
def __(PROJECT_ROOT, mo, os):
    # Rutas de datos
    RAW_DIR = PROJECT_ROOT / "data" / "raw"
    PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
    
    # Verificamos archivos clave
    ventas_raw_exists = os.path.exists(RAW_DIR / "ventas.csv")
    # Buscamos el parquet procesado (puede estar en una subcarpeta según el pipeline)
    processed_files = list(PROCESSED_DIR.glob("**/*.parquet"))
    ventas_processed_exists = len(processed_files) > 0
    
    if ventas_processed_exists:
        processed_path = processed_files[0]
        data_status_msg = "✅ Datos listos para análisis"
        status_color = "green"
    elif ventas_raw_exists:
        processed_path = None
        data_status_msg = "⚠️ Datos crudos descargados, pero no procesados"
        status_color = "orange"
    else:
        processed_path = None
        data_status_msg = "❌ No hay datos detectados"
        status_color = "red"

    status_indicator = mo.callout(data_status_msg, kind=status_color)
    return (
        PROCESSED_DIR,
        RAW_DIR,
        data_status_msg,
        processed_path,
        status_color,
        status_indicator,
        ventas_processed_exists,
        ventas_raw_exists,
    )


@app.cell
def __(mo, processed_path, ventas_processed_exists):
    # Carga de datos reactiva
    if ventas_processed_exists and processed_path:
        df = pd.read_parquet(processed_path)
        df['date'] = pd.to_datetime(df['date'])
    else:
        df = pd.DataFrame()
    
    return (df,)


@app.cell
def __(df, mo):
    # UI Elements para la Sidebar
    mo.stop(df.empty, mo.sidebar(mo.md("### ⚠️ Sin datos\nUsa la pestaña de Orquestación para descargar y procesar los datos.")))

    # Selectores
    families = sorted(df['family'].unique().tolist())
    family_select = mo.ui.multiselect(
        options=families, 
        label="Familias de Productos",
        value=families[:5]
    )
    
    date_range = mo.ui.date_range(
        start=df['date'].min(),
        stop=df['date'].max(),
        label="Rango de Fechas"
    )

    top_n_slider = mo.ui.slider(
        start=5, stop=20, step=1, value=10, 
        label="Top Categorías"
    )

    # Sidebar Layout
    sidebar = mo.sidebar([
        mo.md("# 🛠️ Controles"),
        mo.md("---"),
        mo.md("### 🔍 Filtros Globales"),
        family_select,
        date_range,
        top_n_slider,
        mo.md("---"),
        mo.md("### ℹ️ Info"),
        mo.md(f"**Registros totales:** {len(df):,}"),
        mo.md(f"**Última fecha:** {df['date'].max().strftime('%Y-%m-%d')}")
    ])
    
    return date_range, families, family_select, sidebar, top_n_slider


@app.cell
def __(date_range, df, family_select, mo, pd):
    # Filtrado reactivo
    mo.stop(df.empty)
    
    filtered_df = df[
        (df['family'].isin(family_select.value)) & 
        (df['date'] >= pd.to_datetime(date_range.start)) & 
        (df['date'] <= pd.to_datetime(date_range.stop))
    ]
    
    return (filtered_df,)


@app.cell
def __(
    PROJECT_ROOT,
    download_hf_dataset,
    mo,
    os,
    pipeline_available,
    run_full_pipeline,
    status_indicator,
):
    # PESTAÑA 1: GESTIÓN DE DATOS (Orquestación)
    
    # Botones de acción
    download_btn = mo.ui.button(
        label="📥 Descargar Datos de HF", 
        on_click=lambda _: download_hf_dataset(),
        kind="neutral"
    )
    
    pipeline_btn = mo.ui.button(
        label="🚀 Ejecutar Pipeline Completo", 
        on_click=lambda _: run_full_pipeline(),
        kind="primary",
        disabled=not pipeline_available
    )

    # Tabla de archivos
    def get_file_info(directory):
        files_info = []
        if os.path.exists(directory):
            for f in os.scandir(directory):
                if f.is_file():
                    stats = f.stat()
                    files_info.append({
                        "Archivo": f.name,
                        "Tamaño (MB)": round(stats.st_size / (1024 * 1024), 2),
                        "Modificado": os.path.getmtime(f.path)
                    })
        return pd.DataFrame(files_info)

    raw_files_df = get_file_info(PROJECT_ROOT / "data" / "raw")
    processed_files_df = get_file_info(PROJECT_ROOT / "data" / "processed" / "store_sales_hf")

    orchestration_tab = mo.vstack([
        mo.md("## 🏗️ Orquestación de Datos (ETL)"),
        status_indicator,
        mo.md("Este panel permite gestionar el flujo de datos desde la extracción hasta el procesamiento final."),
        mo.hstack([
            mo.vstack([
                mo.md("### 1. Extracción (Hugging Face)"),
                mo.md("Obtiene los datos crudos del repositorio oficial."),
                download_btn
            ]),
            mo.vstack([
                mo.md("### 2. Procesamiento (Pipeline)"),
                mo.md("Limpia, transforma y genera el dataset analítico."),
                pipeline_btn
            ])
        ], justify="space-around", gap=2),
        mo.md("---"),
        mo.md("### 📂 Estado del Almacenamiento"),
        mo.accordion({
            "Archivos Crudos (data/raw)": mo.ui.table(raw_files_df) if not raw_files_df.empty else mo.md("_No hay archivos_"),
            "Archivos Procesados (data/processed)": mo.ui.table(processed_files_df) if not processed_files_df.empty else mo.md("_No hay archivos_")
        })
    ])
    
    return (
        download_btn,
        get_file_info,
        orchestration_tab,
        pipeline_btn,
        processed_files_df,
        raw_files_df,
    )


@app.cell
def __(filtered_df, mo, px, top_n_slider):
    # PESTAÑA 2: ANÁLISIS DE VENTAS (Dashboard)
    mo.stop(filtered_df.empty)

    # Métricas Globales
    total_sales = filtered_df['sales'].sum()
    avg_sales = filtered_df['sales'].mean()
    unique_families = filtered_df['family'].nunique()
    
    metrics = mo.hstack([
        mo.stat(value=f"${total_sales:,.0f}", label="Ventas Totales", caption="Suma filtrada"),
        mo.stat(value=f"${avg_sales:,.2f}", label="Venta Media", caption="Promedio por registro"),
        mo.stat(value=str(unique_families), label="Categorías", caption="Familias activas")
    ], justify="space-between")

    # Gráficos
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    fig_line = px.line(daily_sales, x='date', y='sales', title='Tendencia Temporal de Ventas')
    
    family_sales = filtered_df.groupby('family')['sales'].sum().sort_values(ascending=False).head(top_n_slider.value).reset_index()
    fig_bar = px.bar(family_sales, x='sales', y='family', orientation='h', title=f'Top {top_n_slider.value} Categorías', color='sales')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})

    # Botón de Descarga de Datos Filtrados
    csv_download = mo.ui.download(
        data=filtered_df.to_csv(index=False),
        filename="analisis_ventas_filtrado.csv",
        label="📥 Descargar selección actual"
    )

    analysis_tab = mo.vstack([
        mo.md("## 📊 Análisis Exploratorio"),
        metrics,
        mo.md("---"),
        mo.hstack([
            mo.as_html(fig_line),
            mo.as_html(fig_bar)
        ], widths=[1.5, 1]),
        mo.md("---"),
        mo.hstack([
            mo.md("### 📥 Exportar Resultados"),
            csv_download
        ], justify="start", align="center")
    ])

    return (
        analysis_tab,
        avg_sales,
        csv_download,
        daily_sales,
        family_sales,
        fig_bar,
        fig_line,
        metrics,
        total_sales,
        unique_families,
    )


@app.cell
def __(analysis_tab, mo, orchestration_tab, sidebar):
    # RENDERIZADO FINAL
    # Mostramos la sidebar y las pestañas principales
    layout = mo.vstack([
        sidebar,
        mo.tabs({
            "📊 Análisis de Ventas": analysis_tab,
            "🏗️ Orquestación (ETL)": orchestration_tab
        })
    ])
    
    layout
    return (layout,)


if __name__ == "__main__":
    app.run()
