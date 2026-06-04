"""
tfm_io.py — Funciones de entrada/salida de datos del TFM.

Centraliza la lectura de las fuentes originales (DGT, INE) y el guardado
de los datasets procesados, para que los notebooks queden limpios.
"""
import pandas as pd
from pathlib import Path

# Carácter comodín que la DGT usa para "valor desconocido" (¡ en latin-1)
NA_VALUES_DGT = ["\xa1", ""]


def cargar_dgt(ruta, usecols=None):
    """
    Lee un fichero de microdatos del parque de vehículos de la DGT.

    Parameters
    ----------
    ruta : str | Path
        Ruta al fichero .txt de la DGT (separado por '|', encoding latin-1).
    usecols : list[str], opcional
        Subconjunto de columnas a leer (reduce el uso de memoria).

    Returns
    -------
    pd.DataFrame
        Datos en bruto, todas las columnas como texto (dtype=str).
    """
    return pd.read_csv(
        ruta, sep="|", encoding="latin-1", low_memory=False,
        dtype=str, na_values=NA_VALUES_DGT, usecols=usecols,
    )


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
    size_mb = ruta.stat().st_size / (1024 ** 2)
    print(f"Guardado: {ruta}  ({len(df):,} filas, {size_mb:.1f} MB)")

