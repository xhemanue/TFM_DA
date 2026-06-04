"""
tfm_limpieza.py — Funciones de limpieza y estandarización de texto.

Pensadas para vectorizar operaciones habituales de Data Wrangling sin bucles
fila a fila, siguiendo buenas prácticas de Pandas.
"""
import pandas as pd


def estandarizar_texto(df, columnas):
    """
    Normaliza columnas de texto: quita espacios sobrantes y pasa a mayúsculas.

    Útil para unificar categorías duplicadas por formato (p. ej. 'Seat' / 'SEAT ').

    Parameters
    ----------
    df : pd.DataFrame
    columnas : list[str]
        Columnas de texto a estandarizar.

    Returns
    -------
    pd.DataFrame
        El mismo DataFrame con las columnas indicadas estandarizadas.
    """
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].str.strip().str.upper()
    return df


def a_categoria(df, columnas):
    """Convierte las columnas indicadas al tipo 'category' (ahorra memoria)."""
    for col in columnas:
        if col in df.columns:
            df[col] = df[col].astype("category")
    return df


def resumen_nulos(df):
    """
    Devuelve un resumen del porcentaje de nulos por columna, ordenado de mayor a menor.

    Returns
    -------
    pd.DataFrame
        Columnas: ['columna', 'n_nulos', 'pct_nulos'].
    """
    n = df.isna().sum()
    pct = (df.isna().mean() * 100).round(2)
    out = (
        pd.DataFrame({"columna": n.index, "n_nulos": n.values, "pct_nulos": pct.values})
        .sort_values("pct_nulos", ascending=False)
        .reset_index(drop=True)
    )
    return out

def estandarizar_nombres_columnas(df):
    """
    Estandariza los nombres de columna: elimina espacios sobrantes, pasa a
    minúsculas y reemplaza espacios internos por guiones bajos.

    Genérica y reutilizable entre proyectos.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        El mismo DataFrame con los nombres de columna estandarizados.
    """
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(" ", "_"))
    return df

def corregir_decimales(df, columnas, separador_origen=",", separador_destino=".", tipo_float="float32"):
    """
    Convierte columnas numéricas en formato texto a tipo flotante, 
    reemplazando el separador decimal especificado.

    Parameters
    ----------
    df : pd.DataFrame
    columnas : list[str]
        Columnas con formato string que se desean transformar.
    separador_origen : str, default ','
        El carácter que representa los decimales en el dataset original.
    separador_destino : str, default '.'
        El carácter decimal al que se desea convertir (habitualmente '.').
    tipo_float : str, default 'float32'
        Precisión del float deseado ('float32' o 'float64').

    Returns
    -------
    pd.DataFrame
        El mismo DataFrame con las columnas numéricas corregidas.
    """
    for col in columnas:
        if col in df.columns:
            # Forzamos a str, reemplazamos el separador dinámicamente y coaccionamos
            df[col] = df[col].astype(str).str.replace(separador_origen, separador_destino, regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(tipo_float)
    return df

def corregir_enteros_nullable(df, mapeo_columnas):
    """
    Convierte columnas a tipos enteros de Pandas que admiten valores nulos (Nullable Integers),
    coaccionando errores a NaN.

    Evita que Pandas transforme columnas de enteros con nulos a tipo float.

    Parameters
    ----------
    df : pd.DataFrame
    mapeo_columnas : dict
        Diccionario donde las claves son los nombres de las columnas y los valores
        son el tipo de entero en formato string (ej: {'cilindrada': 'Int16', 'num_titulares': 'Int8'}).

    Returns
    -------
    pd.DataFrame
        El mismo DataFrame con las columnas de enteros corregidas.
    """
    for col, tipo_entero in mapeo_columnas.items():
        if col in df.columns:
            # pd.to_numeric convierte a float/int temporalmente (manejando errores)
            # y .astype() lo fuerza al entero nullable de Pandas (Int8, Int16, etc.)
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(tipo_entero)
    return df