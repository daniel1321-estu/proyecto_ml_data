import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuración de la página (Siguiendo el estilo del profe)
st.set_page_config(page_title="Dashboard Control de Ventas", page_icon="📈", layout="wide")

# 2. Título
st.title("📊 Dashboard de Análisis de Ventas (Store Sales)")

# 3. Cargar datos con la metodología del profe
@st.cache_data
def load_data():
    # Ruta al archivo procesado por nuestro pipeline
    file_path = "data/processed/ventas_limpias.csv"
    
    if not os.path.exists(file_path):
        # Si no existe el CSV, intentamos con el Parquet
        parquet_path = "data/processed/store_sales_hf/sales_processed.parquet"
        if os.path.exists(parquet_path):
            df = pd.read_parquet(parquet_path)
        else:
            return None
    else:
        df = pd.read_csv(file_path)
    
    # Limpieza y preparación (similar a la del profe)
    df['date'] = pd.to_datetime(df['date'])
    df['Año'] = df['date'].dt.year
    df['Mes'] = df['date'].dt.month_name()
    df['family'] = df['family'].astype(str)
    return df

try:
    df = load_data()
    if df is None:
        st.error("❌ No se encontraron datos. Por favor, ejecuta el pipeline primero: `python main.py`")
        st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# 4. Sidebar - Filtros (Metodología Slider + Multiselect)
st.sidebar.header("Filtros")

# Filtro Año (Slider)
min_year = int(df['Año'].min())
max_year = int(df['Año'].max())

if min_year == max_year:
    st.sidebar.write(f"Año disponible: **{min_year}**")
    selected_years = (min_year, max_year)
else:
    selected_years = st.sidebar.slider("Selecciona el rango de años", min_year, max_year, (min_year, max_year))

# Filtro Familia de Producto (Multiselect)
all_families = sorted(df['family'].unique().tolist())
selected_families = st.sidebar.multiselect("Selecciona Categoría(s)", all_families, default=all_families[:5])

# Aplicar filtros
df_filtered = df[
    (df['Año'] >= selected_years[0]) &
    (df['Año'] <= selected_years[1]) &
    (df['family'].isin(selected_families))
]

if df_filtered.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados.")
    st.stop()

# 5. KPIs (Siguiendo el formato col1, col2...)
col1, col2, col3, col4 = st.columns(4)

total_sales = df_filtered['sales'].sum()
avg_sales = df_filtered['sales'].mean()
top_category = df_filtered.groupby('family')['sales'].sum().idxmax()
total_records = len(df_filtered)

col1.metric("Ventas Totales", f"${total_sales:,.2f}")
col2.metric("Promedio de Venta", f"${avg_sales:,.2f}")
col3.metric("Categoría Top", top_category)
col4.metric("Total Registros", f"{total_records:,}")

st.markdown("---")

# 6. Gráficos (Estructura de columnas del profe)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Ventas Totales por Año")
    sales_by_year = df_filtered.groupby('Año')['sales'].sum().reset_index()
    fig_year = px.bar(sales_by_year, x='Año', y='sales', 
                      title="Ventas por Año", 
                      color_discrete_sequence=['#4C78A8'],
                      labels={'sales': 'Ventas ($)', 'Año': 'Año'})
    st.plotly_chart(fig_year, use_container_width=True)

with col_right:
    st.subheader("Distribución de Ventas por Categoría")
    sales_by_family = df_filtered.groupby('family')['sales'].sum().reset_index()
    fig_pie = px.pie(sales_by_family, values='sales', names='family', 
                     title="Distribución por Familia", 
                     hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# Gráfico Horizontal de Top Productos/Categorías
st.subheader("Top 10 Categorías por Volumen de Ventas")
top_10_families = df_filtered.groupby('family')['sales'].sum().nlargest(10).reset_index()
fig_top10 = px.bar(top_10_families, x='sales', y='family', 
                   orientation='h', 
                   title="Top 10 Categorías", 
                   color='sales', 
                   color_continuous_scale='Viridis',
                   labels={'sales': 'Ventas Totales ($)', 'family': 'Categoría'})
fig_top10.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_top10, use_container_width=True)

st.markdown("---")
# 7. Datos Detallados
st.subheader("Datos Detallados")
st.dataframe(df_filtered.head(500)) # Mostramos los primeros 500 para no saturar el navegador
