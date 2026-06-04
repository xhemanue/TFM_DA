"""
tfm_eda.py — Funciones de perfilado y análisis exploratorio.
"""
import pandas as pd


def eda_preliminar(df, cols_in_outlier=None, cols_notin_outlier=None):
    """
    Realiza un análisis exploratorio preliminar (EDA) sobre un DataFrame.

    El análisis comprende:
        - Inspección estructural y de tipos
        - Detección de datos faltantes y duplicados
        - Análisis de variables categóricas
        - Detección de valores atípicos (outliers) mediante el método IQR
        - Resumen estadístico numérico

    Parameters
    ----------
    df : pd.DataFrame
        El conjunto de datos que se desea analizar.
    cols_in_outlier : list of str, optional
        Columnas específicas para detectar outliers. Si es None, 
        se analizan todas las columnas numéricas.
    cols_notin_outlier : list of str, optional
        Columnas numéricas que se deben excluir específicamente 
        del análisis de outliers (ej. IDs, años).

    Returns
    -------
    None
        La función imprime y muestra los resultados directamente en el notebook.
    """
    from IPython.display import display # Importación segura por si lo usas en un .py externo

    print("\n>>> INFO ESTRUCTURAL")
    df.info() 

    secciones = {
        "Muestra de Datos": df.sample(5, random_state=42),
        "Dimensiones": f"El conjunto de datos tiene {df.shape[0]:,} filas y {df.shape[1]} columnas.",
        "Valores Nulos (%)": df.isna().mean().mul(100).sort_values(ascending=False).head(10),
        "Registros Duplicados": f"Se detectaron {df.duplicated().sum():,} filas repetidas."
    }

    for titulo, contenido in secciones.items():
        print(f"\n>>> {titulo.upper()}")
        display(contenido)

    print("\n>>> ANÁLISIS DE CATEGÓRICAS (Top 10 %)")
    cols_cat = df.select_dtypes(include=['object', 'category']).columns
    if len(cols_cat) > 0:
        for col in cols_cat:
            print(f"\nDistribución en: {col}")
            # Multiplicamos por 100 para ver un % real (ej: 45.5%) en lugar de 0.455
            display(df[col].value_counts(normalize=True).mul(100).round(2).head(10))
    else:
        print("No se encontraron variables categóricas.")

    print("\n>>> DETECCIÓN DE POSIBLES OUTLIERS (MÉTODO IQR)")
    outlier_report = {}    
    
    if cols_in_outlier:
        cols_num = cols_in_outlier
    else:
        cols_num = df.select_dtypes(include=['number']).columns.tolist()

    if cols_notin_outlier:
        cols_num = [col for col in cols_num if col not in cols_notin_outlier]
    
    for col in cols_num:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        
        # Optimización: sumamos booleanos en lugar de crear un DataFrame nuevo
        cantidad_outliers = ((df[col] < limite_inferior) | (df[col] > limite_superior)).sum()
        if cantidad_outliers > 0:
            outlier_report[col] = cantidad_outliers
            
    if outlier_report:
        df_outliers = pd.Series(outlier_report, name="Cantidad de Outliers").to_frame()
        # Añadimos el % de outliers sobre el total para dar más contexto
        df_outliers["% del Total"] = (df_outliers["Cantidad de Outliers"] / len(df) * 100).round(2)
        display(df_outliers.sort_values(by="Cantidad de Outliers", ascending=False))
    else:
        print("No se detectaron outliers significativos mediante IQR.")

    print("\n>>> TENDENCIA CENTRAL Y DISPERSIÓN (NUMÉRICAS)")
    display(df.describe().T)



