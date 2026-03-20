import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Tablero de Insights de Retail",
    page_icon="🏪",
    layout="wide",
)

def main():
    # --- Cargar Datos ---
    @st.cache_data
    def load_data():
        base_path = Path(__file__).resolve().parent.parent.parent
        data_path = base_path / "data" / "processed" / "ventas_limpias.csv"
        
        if not data_path.exists():
            st.error(f"Archivo de datos no encontrado en: {data_path}")
            return None
            
        try:
            # Lectura optimizada para CSV grande
            df = pd.read_csv(data_path)
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            st.error(f"Error al cargar los datos: {e}")
            return None

    df = load_data()

    if df is None:
        st.stop()

    # --- Filtros de la Barra Lateral ---
    st.sidebar.header("📊 Filtros Globales")

    # 1. Filtro de Rango de Fechas
    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.sidebar.date_input(
        "Rango de Fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # 2. Selección de Tienda (Categórico)
    unique_stores = sorted(df["store_nbr"].unique())
    selected_stores = st.sidebar.multiselect(
        "Seleccionar Tiendas",
        options=unique_stores,
        default=unique_stores[:10] if len(unique_stores) > 10 else unique_stores,
        help="Filtrar por número de tienda"
    )

    # 3. Familia de Productos (Categórico)
    unique_families = sorted(df["family"].unique())
    selected_families = st.sidebar.multiselect(
        "Familias de Productos",
        options=unique_families,
        default=unique_families,
        help="Filtrar por categoría"
    )

    # 4. Filtro de Volumen de Ventas (Numérico)
    min_sales_val = float(df["sales"].min())
    max_sales_val = float(df["sales"].max())
    sales_range = st.sidebar.slider(
        "Rango de Valor de Ventas",
        min_value=min_sales_val,
        max_value=max_sales_val,
        value=(min_sales_val, max_sales_val)
    )

    # 5. Filtro de Promociones (Numérico)
    min_promo = int(df["onpromotion"].min())
    max_promo = int(df["onpromotion"].max())
    promo_range = st.sidebar.slider(
        "Artículos en Promoción",
        min_value=min_promo,
        max_value=max_promo,
        value=(min_promo, max_promo)
    )

    # --- Lógica de Filtrado de Datos ---
    # Validar que el rango de fechas sea una tupla de dos elementos para evitar errores
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        # Fallback seguro si la selección de fecha es incompleta
        start_date, end_date = min_date, max_date

    mask = (
        (df["store_nbr"].isin(selected_stores)) &
        (df["family"].isin(selected_families)) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date)) &
        (df["sales"] >= sales_range[0]) &
        (df["sales"] <= sales_range[1]) &
        (df["onpromotion"] >= promo_range[0]) & 
        (df["onpromotion"] <= promo_range[1])
    )
    
    df_filtered = df.loc[mask]

    # --- Interfaz Principal del Tablero ---
    st.title("🚀 Tablero de Rendimiento de Retail")
    st.markdown("Análisis interactivo de datos de ventas y promociones limpios.")
    st.divider()

    # --- Fila de KPIs ---
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    with kpi_col1:
        total_sales = df_filtered["sales"].sum()
        st.metric("Ingresos Totales", f"${total_sales:,.0f}")
    
    with kpi_col2:
        avg_sales = df_filtered["sales"].mean()
        st.metric("Promedio por Transacción", f"${avg_sales:,.2f}")
        
    with kpi_col3:
        max_sale = df_filtered["sales"].max()
        st.metric("Venta Máxima", f"${max_sale:,.0f}")
        
    with kpi_col4:
        promo_count = df_filtered["onpromotion"].sum()
        st.metric("Volumen de Promociones", f"{promo_count:,.0f}")

    with kpi_col5:
        records = len(df_filtered)
        st.metric("Registros Encontrados", f"{records:,}")

    st.divider()

    # --- Fila de Gráficos 1 ---
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:
        st.subheader("📈 Tendencias de Ingresos")
        if not df_filtered.empty:
            ts_data = df_filtered.groupby("date")["sales"].sum().reset_index()
            fig_ts = px.area(ts_data, x="date", y="sales", title="Ventas a lo largo del tiempo", labels={"date": "Fecha", "sales": "Ventas"})
            st.plotly_chart(fig_ts, use_container_width=True)
        else:
            st.info("No hay datos para mostrar con los filtros actuales.")

    with row1_col2:
        st.subheader("📦 Principales Familias de Productos")
        if not df_filtered.empty:
            family_data = df_filtered.groupby("family")["sales"].sum().nlargest(10).reset_index()
            fig_fam = px.bar(family_data, y="family", x="sales", orientation='h', color="sales", title="Top 10 Familias", labels={"family": "Familia", "sales": "Ventas"})
            st.plotly_chart(fig_fam, use_container_width=True)
        else:
            st.info("No hay datos para mostrar.")

    # --- Fila de Gráficos 2 ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("🏪 Distribución de Ventas por Tienda")
        if not df_filtered.empty:
            store_data = df_filtered.groupby("store_nbr")["sales"].sum().reset_index()
            fig_store = px.pie(store_data, values="sales", names="store_nbr", hole=0.4, title="Ventas por Tienda")
            st.plotly_chart(fig_store, use_container_width=True)
        else:
            st.info("No hay datos para mostrar.")

    with row2_col2:
        st.subheader("🎯 Correlación Ventas vs Promociones")
        if not df_filtered.empty:
            # Muestreo para rendimiento
            sample_size = min(len(df_filtered), 3000)
            scatter_sample = df_filtered.sample(sample_size) if len(df_filtered) > 0 else df_filtered
            fig_scatter = px.scatter(
                scatter_sample, 
                x="onpromotion", 
                y="sales", 
                color="family",
                opacity=0.6,
                hover_data=["store_nbr", "date"],
                title="Ventas vs Promociones",
                labels={"onpromotion": "En Promoción", "sales": "Ventas", "family": "Familia"}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No hay datos para mostrar.")

if __name__ == "__main__":
    main()
