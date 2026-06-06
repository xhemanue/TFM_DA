"""
tfm_io.py — Funciones de entrada/salida de datos del TFM.

Centraliza la lectura de las fuentes originales (DGT, INE) y el guardado
de los datasets procesados, para que los notebooks queden limpios.
"""
import pandas as pd
from pathlib import Path

def cargar_parquet(nombre_archivo, directorio_base):
    """
    Carga un archivo parquet de forma segura, validando su existencia.

    Si el archivo no existe o falla la carga, detiene la ejecución del notebook
    con un mensaje controlado, evitando un traceback largo.

    Parameters
    ----------
    nombre_archivo : str
        Nombre del archivo .parquet a cargar (ej: 'dataset_fusionado.parquet').
    directorio_base : pathlib.Path
        Ruta del directorio donde se encuentra el archivo.

    Returns
    -------
    pd.DataFrame
        El DataFrame cargado desde el archivo parquet.
    """
    ruta = directorio_base / nombre_archivo
    try:
        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encuentra {ruta.resolve()}. Ejecuta antes el notebook correspondiente."
            )
        df = pd.read_parquet(ruta)
        print(
            f"Cargado exitosamente: {df.shape[0]:,} filas x {df.shape[1]} columnas"
        )
        return df
    except FileNotFoundError as e:
        raise SystemExit(f"ERROR DE CARGA: {e}")
    except Exception as e:
        raise SystemExit(f"ERROR INESPERADO al leer {ruta.name}: {e}")


def guardar_parquet(df, ruta):
    """Guarda un DataFrame en Parquet, creando la carpeta si no existe."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta, index=False)
    
    # Cálculo dinámico del tamaño para mostrar KB o MB
    size_bytes = ruta.stat().st_size
    if size_bytes < (1024 ** 2):
        size_kb = size_bytes / 1024
        print(f"Guardado: {ruta}  ({len(df):,} filas, {size_kb:.1f} KB)")
    else:
        size_mb = size_bytes / (1024 ** 2)
        print(f"Guardado: {ruta}  ({len(df):,} filas, {size_mb:.1f} MB)")
 
 
def guardar_csv_es(df, ruta):
    """
    Guarda un DataFrame en CSV con las convenciones españolas para que Excel y
    Power BI lo lean bien: separador ';', coma decimal y codificación
    'utf-8-sig' (BOM), de modo que las tildes y la 'ñ' se visualicen correctamente.

    Parameters
    ----------
    df : pd.DataFrame
        Tabla a exportar.
    ruta : str | Path
        Ruta de destino del fichero .csv (se crea la carpeta si no existe).
    """
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False, sep=";", decimal=",", encoding="utf-8-sig")
    
    # Cálculo dinámico del tamaño para mostrar KB o MB
    size_bytes = ruta.stat().st_size
    if size_bytes < (1024 ** 2):
        size_kb = size_bytes / 1024
        print(f"Guardado: {ruta}  ({len(df):,} filas, {size_kb:.1f} KB)")
    else:
        size_mb = size_bytes / (1024 ** 2)
        print(f"Guardado: {ruta}  ({len(df):,} filas, {size_mb:.1f} MB)")