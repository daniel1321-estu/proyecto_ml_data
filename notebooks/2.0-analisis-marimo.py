import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import os
    return mo, pd, px, os


@app.cell
def __(mo, os, pd):
    # Intentamos cargar los datos desde la ruta del proyecto
    PROCESSED_PATH = "data/processed/store_sales_hf/sales_processed.parquet"

    if os.path.exists(PROCESSED_PATH):
        df = pd.read_parquet(PROCESSED_PATH)
        df['date'] = pd.to_datetime(df['date'])
        data_status = mo.md("✅ **Datos cargados correctamente.**")
    else:
        df = pd.DataFrame()
        data_status = mo.md("❌ **No se encontraron datos.** Por favor, ejecuta el pipeline de descarga y procesamiento primero.")
    
    return PROCESSED_PATH, df, data_status


@app.cell
def __(data_status, mo):
    mo.md(
        f"""
        # 📈 Análisis Interactivo de Ventas (Marimo Edition)
        
        {data_status}
        
        Este notebook reactivo permite explorar las tendencias de ventas con un layout profesional.
        """
    )
    return


@app.cell
def __(df, mo):
    # UI Elements para filtrado
    mo.stop(df.empty, mo.md("Esperando datos..."))

    families = sorted(df['family'].unique().tolist())
    family_select = mo.ui.multiselect(
        options=families, 
        label="Filtrar por Categoría (Family)",
        value=families[:5] # Por defecto las primeras 5
    )
    
    date_range = mo.ui.date_range(
        start=df['date'].min(),
        stop=df['date'].max(),
        label="Rango de Fechas"
    )

    return date_range, families, family_select


@app.cell
def __(date_range, df, family_select, mo):
    # Lógica de filtrado reactivo
    mo.stop(df.empty)
    
    filtered_df = df[
        (df['family'].isin(family_select.value)) & 
        (df['date'] >= pd.to_datetime(date_range.start)) & 
        (df['date'] <= pd.to_datetime(date_range.stop))
    ]
    
    return (filtered_df,)


@app.cell
def __(filtered_df, mo, px):
    # Cálculo de métricas
    total_sales = filtered_df['sales'].sum()
    avg_sales = filtered_df['sales'].mean()
    num_records = len(filtered_df)

    metrics = mo.hstack([
        mo.stat(value=f"${total_sales:,.2f}", label="Ventas Totales", caption="En el periodo/categorías seleccionadas"),
        mo.stat(value=f"${avg_sales:,.2f}", label="Venta Promedio", caption="Por registro"),
        mo.stat(value=f"{num_records:,}", label="Registros", caption="Total de filas filtradas")
    ], justify="start")

    return avg_sales, metrics, num_records, total_sales


@app.cell
def __(filtered_df, mo, px):
    # Visualizaciones
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    fig_line = px.line(daily_sales, x='date', y='sales', title='Evolución Temporal de Ventas')
    fig_line.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    
    family_sales = filtered_df.groupby('family')['sales'].sum().sort_values(ascending=True).reset_index()
    fig_bar = px.bar(family_sales, x='sales', y='family', orientation='h', title='Ventas por Categoría', color='sales')
    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    # Layout de las celdas usando mo.vstack y mo.hstack (como en tus imágenes)
    dashboard = mo.vstack([
        mo.md("### Controles de Filtrado"),
        mo.hstack([family_select, date_range], justify="start"),
        mo.hr(),
        metrics,
        mo.hstack([
            mo.as_html(fig_line),
            mo.as_html(fig_bar)
        ], widths=[1.5, 1])
    ])

    return dashboard, daily_sales, family_sales, fig_bar, fig_line


@app.cell
def __(dashboard):
    dashboard
    return


if __name__ == "__main__":
    app.run()
