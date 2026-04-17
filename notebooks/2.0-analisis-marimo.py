import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md(r"""
    # 🎨 Guía de Diseño Interactivo en Marimo

    En esta sección aprenderemos a organizar interfaces profesionales utilizando los componentes de diseño de Marimo. Esta guía sirve como base para el análisis de ventas que se encuentra al final.
    """)
    return


@app.cell
def _(mo):
    # SECCIÓN 1: ORGANIZACIÓN BÁSICA
    mo.md(
        r"""
        ## 1. Organización en Filas y Columnas
        La base de cualquier diseño son los *Stacks*. Permiten alinear elementos de forma horizontal o vertical.
        """
    )

    fila_ejemplo = mo.hstack(
        [mo.ui.text(label="Entrada de texto"), mo.ui.slider(1, 10, label="Nivel de ajuste")],
        justify="start",
    )

    columna_ejemplo = mo.vstack(
        [mo.ui.text(label="Descripción"), mo.ui.number(1, 10, label="Cantidad")]
    )

    mo.tabs({
        "Alineación Horizontal": mo.vstack([
            mo.md("Usa `mo.hstack` para colocar elementos uno al lado del otro:"),
            fila_ejemplo
        ]),
        "Alineación Vertical": mo.vstack([
            mo.md("Usa `mo.vstack` para apilar elementos:"),
            columna_ejemplo
        ])
    })
    return


@app.cell
def _(mo):
    # SECCIÓN 2: CONTROL DE DISEÑO AVANZADO
    mo.md(
        r"""
        ## 2. Personalización del Espacio
        Podemos controlar exactamente cómo se distribuyen los elementos usando parámetros de alineación y espaciado.
        """
    )

    justify = mo.ui.dropdown(
        ["start", "center", "end", "space-between", "space-around"],
        value="space-between",
        label="Justificación horizontal",
    )
    align = mo.ui.dropdown(
        ["start", "center", "end", "stretch"], value="center", label="Alineación vertical"
    )
    gap = mo.ui.number(start=0, step=0.25, stop=2, value=0.5, label="Espacio entre objetos")
    wrap = mo.ui.checkbox(label="Ajuste de línea (wrap)")

    size = mo.ui.slider(label="Tamaño de bloques", start=100, stop=400, value=150)

    mo.hstack([justify, align, gap, wrap], justify="center", gap=2)
    return align, gap, justify, size, wrap


@app.cell
def _(align, gap, justify, mo, size, wrap):
    # Visualización dinámica de la personalización
    def crear_bloque(nombre):
        return mo.callout(
            mo.center(mo.md(f"### {nombre}")), 
            kind="neutral"
        ).style({"width": f"{size.value}px", "height": f"{size.value}px"})

    bloques = [crear_bloque(n) for n in ["A", "B", "C", "D"]]

    demo_layout = mo.hstack(
        bloques,
        align=align.value,
        justify=justify.value,
        gap=gap.value,
        wrap=wrap.value,
    )

    mo.vstack([
        mo.center(size),
        mo.md("### Vista Previa del Diseño"),
        demo_layout
    ])
    return


@app.cell
def _(mo):
    # SECCIÓN 3: CONTENEDORES Y ESTRUCTURA
    mo.md(
        r"""
        ## 3. Estructuras de Información
        Para análisis complejos, utilizamos **Acordeones** para ocultar detalles y **Pestañas** para separar secciones.
        """
    )

    ejemplo_estructura = mo.accordion({
        "📈 Visualización de Datos": mo.md("Aquí se explicaría cómo integrar gráficos de Plotly."),
        "🧮 Lógica de Negocio": mo.md("Detalles sobre los cálculos de ventas y proyecciones."),
        "📂 Gestión de Archivos": mo.md("Estado de los archivos en las carpetas `data/raw` y `data/processed`.")
    })

    ejemplo_estructura
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    # 📊 Laboratorio de Análisis de Ventas
    A continuación, aplicamos todos los conceptos de diseño anteriores para explorar los datos reales del proyecto.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import os
    from pathlib import Path

    # Localización de rutas
    ROOT = Path(os.getcwd()).resolve()
    if ROOT.name == "notebooks":
        ROOT = ROOT.parent

    DATA_PATH = ROOT / "data" / "processed" / "store_sales_hf" / "sales_processed.parquet"

    if DATA_PATH.exists():
        df_ventas = pd.read_parquet(DATA_PATH)
        df_ventas['date'] = pd.to_datetime(df_ventas['date'])
    else:
        df_ventas = pd.DataFrame()

    return df_ventas, mo, pd, px


@app.cell
def _(df_ventas, mo):
    mo.stop(df_ventas.empty, mo.md("### ⚠️ No hay datos disponibles. Por favor, ejecuta el pipeline."))

    # Sidebar de Control
    familias_prod = sorted(df_ventas['family'].unique().tolist())
    sel_familia = mo.ui.multiselect(familias_prod, value=familias_prod[:3], label="Filtrar por Familia")

    rango_fecha = mo.ui.date_range(
        start=df_ventas['date'].min().date(),
        stop=df_ventas['date'].max().date(),
        label="Rango de Fechas"
    )

    mo.sidebar([
        mo.md("# 🏪 Panel de Control"),
        sel_familia,
        rango_fecha,
        mo.md(f"**Registros analizados:** {len(df_ventas):,}")
    ])
    return rango_fecha, sel_familia


@app.cell
def _(df_ventas, mo, pd, px, rango_fecha, sel_familia):
    mo.stop(df_ventas.empty)

    # Procesamiento y Dashboard
    df_filtrado = df_ventas[
        (df_ventas['family'].isin(sel_familia.value)) & 
        (df_ventas['date'] >= pd.to_datetime(rango_fecha.start)) & 
        (df_ventas['date'] <= pd.to_datetime(rango_fecha.stop))
    ]

    # KPIs en formato Stack
    indicadores = mo.hstack([
        mo.stat(label="Ventas Acumuladas", value=f"${df_filtrado['sales'].sum():,.0f}"),
        mo.stat(label="Venta Promedio", value=f"${df_filtrado['sales'].mean():,.2f}")
    ], justify="space-around")

    grafico = px.line(
        df_filtrado.groupby('date')['sales'].sum().reset_index(), 
        x='date', y='sales', 
        title="Evolución Temporal de Ventas"
    )

    mo.vstack([
        indicadores,
        mo.md("---"),
        mo.as_html(grafico)
    ])
    return


if __name__ == "__main__":
    app.run()
