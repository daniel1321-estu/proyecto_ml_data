import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configuración estética global
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (15, 6)

def plot_time_series(df, title="Análisis de Tendencia Temporal"):
    """Grafica la evolución de ventas diarias."""
    plt.figure(figsize=(15, 6))
    daily = df.groupby('date')['sales'].sum()
    plt.plot(daily.index, daily.values, color='#2ecc71', linewidth=1.5)
    plt.title(f"📈 {title}", fontsize=15)
    plt.xlabel("Fecha")
    plt.ylabel("Ventas Totales")
    plt.show()

def plot_monthly_heatmap(df):
    """Crea un mapa de calor de ventas por mes y año."""
    pivot = df.pivot_table(index='month', columns='year', values='sales', aggfunc='sum')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Ventas Totales'})
    plt.title("📅 Mapa de Calor: Ventas por Mes y Año", fontsize=15)
    plt.ylabel("Mes (1=Enero, 12=Diciembre)")
    plt.xlabel("Año")
    plt.show()

def plot_sales_distribution(df):
    """Analiza la distribución de las ventas para detectar sesgos."""
    plt.figure(figsize=(12, 6))
    sns.histplot(df['sales'], bins=50, kde=True, color='#3498db')
    plt.title("📊 Distribución de Ventas (Frecuencia)", fontsize=15)
    plt.xlabel("Valor de Venta")
    plt.ylabel("Frecuencia")
    plt.show()

def plot_promo_impact(df):
    """Compara ventas con y sin promoción."""
    plt.figure(figsize=(10, 6))
    df_promo = df.copy()
    df_promo['En Promoción'] = df_promo['onpromotion'] > 0
    sns.boxplot(x='En Promoción', y='sales', data=df_promo, palette="Set2")
    plt.title("🚀 Impacto de las Promociones en las Ventas", fontsize=15)
    plt.yscale('log') # Escala logarítmica para ver mejor la diferencia si hay mucha dispersión
    plt.show()

def plot_top_families(df, n=15):
    """Ranking de categorías más vendidas."""
    plt.figure(figsize=(12, 8))
    top = df.groupby('family')['sales'].sum().sort_values(ascending=False).head(n)
    sns.barplot(x=top.values, y=top.index, palette="viridis")
    plt.title(f"🏆 Top {n} Categorías con Mayor Volumen de Ventas", fontsize=15)
    plt.xlabel("Ventas Acumuladas")
    plt.ylabel("Familia de Producto")
    plt.show()

def plot_weekday_analysis(df):
    """Análisis detallado por día de la semana."""
    plt.figure(figsize=(12, 6))
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    sns.barplot(x='weekday', y='sales', data=df, palette="husl", errorbar=None)
    plt.xticks(range(7), dias)
    plt.title("🗓️ Promedio de Ventas por Día de la Semana", fontsize=15)
    plt.xlabel("Día")
    plt.ylabel("Venta Promedio")
    plt.show()
