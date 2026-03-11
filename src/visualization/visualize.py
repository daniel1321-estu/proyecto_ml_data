import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Configuración estética global
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (15, 6)

def plot_time_series(df, title="Análisis de Tendencia Temporal", output_path=None):
    """Grafica la evolución de ventas diarias."""
    plt.figure(figsize=(15, 6))
    daily = df.groupby('date')['sales'].sum()
    plt.plot(daily.index, daily.values, color='#2ecc71', linewidth=1.5)
    plt.title(f"📈 {title}", fontsize=15)
    plt.xlabel("Fecha")
    plt.ylabel("Ventas Totales")
    if output_path:
        plt.savefig(output_path)
        plt.close()
    else:
        plt.show()

def plot_monthly_heatmap(df, output_path=None):
    """Crea un mapa de calor de ventas por mes y año."""
    df_copy = df.copy()
    df_copy['month'] = df_copy['date'].dt.month
    df_copy['year'] = df_copy['date'].dt.year
    pivot = df_copy.pivot_table(index='month', columns='year', values='sales', aggfunc='sum')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Ventas Totales'})
    plt.title("📅 Mapa de Calor: Ventas por Mes y Año", fontsize=15)
    plt.ylabel("Mes (1=Enero, 12=Diciembre)")
    plt.xlabel("Año")
    if output_path:
        plt.savefig(output_path)
        plt.close()
    else:
        plt.show()

def plot_sales_distribution(df, output_path=None):
    """Analiza la distribución de las ventas para detectar sesgos."""
    plt.figure(figsize=(12, 6))
    sns.histplot(df['sales'], bins=50, kde=True, color='#3498db')
    plt.title("📊 Distribución de Ventas (Frecuencia)", fontsize=15)
    plt.xlabel("Valor de Venta")
    plt.ylabel("Frecuencia")
    if output_path:
        plt.savefig(output_path)
        plt.close()
    else:
        plt.show()

def plot_top_families(df, n=15, output_path=None):
    """Ranking de categorías más vendidas."""
    plt.figure(figsize=(12, 8))
    top = df.groupby('family')['sales'].sum().sort_values(ascending=False).head(n)
    sns.barplot(x=top.values, y=top.index, palette="viridis")
    plt.title(f"🏆 Top {n} Categorías con Mayor Volumen de Ventas", fontsize=15)
    plt.xlabel("Ventas Acumuladas")
    plt.ylabel("Familia de Producto")
    if output_path:
        plt.savefig(output_path)
        plt.close()
    else:
        plt.show()

def plot_sales_by_weekday(df, output_path=None):
    """Análisis detallado por día de la semana."""
    plt.figure(figsize=(12, 6))
    df_copy = df.copy()
    df_copy['weekday'] = df_copy['date'].dt.dayofweek
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    sns.barplot(x='weekday', y='sales', data=df_copy, palette="husl", errorbar=None)
    plt.xticks(range(7), dias)
    plt.title("🗓️ Promedio de Ventas por Día de la Semana", fontsize=15)
    plt.xlabel("Día")
    plt.ylabel("Venta Promedio")
    if output_path:
        plt.savefig(output_path)
        plt.close()
    else:
        plt.show()
