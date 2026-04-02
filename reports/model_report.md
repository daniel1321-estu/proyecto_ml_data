# 📊 Reporte de Desempeño de Modelos de Predicción de Ventas

Este reporte detalla la comparación de 5 modelos de Machine Learning evaluados sobre el dataset de ventas procesado. El objetivo es identificar el modelo con mayor capacidad predictiva para el volumen de ventas diarias.

## 📈 Tabla Comparativa de Desempeño

A continuación se presentan las métricas obtenidas tras evaluar los modelos con una muestra representativa de los datos:

| Modelo | Error Absoluto Medio (MAE) | Raíz del Error Cuadrático Medio (RMSE) | Coeficiente de Determinación ($R^2$) | Tiempo de Entrenamiento (s) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **143.3237** | **512.3671** | **0.8006** | **0.70** |
| Decision Tree | 159.9988 | 567.4764 | 0.7554 | 0.13 |
| Gradient Boosting | 197.3557 | 585.9525 | 0.7392 | 3.13 |
| Linear Regression | 434.8845 | 1046.6084 | 0.1681 | 0.03 |
| Ridge Regression | 434.8845 | 1046.6084 | 0.1681 | 0.01 |

## 🏆 Conclusión y Selección

El mejor modelo identificado es el **Random Forest Regressor**, con un **$R^2$ de 0.8006**. 

### Puntos Clave:
1. **Precisión**: Es el modelo que mejor explica la varianza de los datos (80%), superando significativamente a los modelos lineales.
2. **Robustez**: Al ser un conjunto de árboles de decisión, maneja mejor las relaciones no lineales y los valores atípicos en las ventas.
3. **Eficiencia**: Aunque el entrenamiento toma un poco más que un modelo lineal (0.70s), es extremadamente rápido comparado con Gradient Boosting (3.13s), ofreciendo el mejor balance entre precisión y tiempo.

---
*Reporte generado automáticamente por Gemini CLI.*
