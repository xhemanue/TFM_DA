"""
tfm_vis.py — Funciones de visualización y gráficos para el TFM.
"""
import numpy as np
import matplotlib.pyplot as plt

def barras_segmento(serie, titulo, etiqueta_y, orden_segmentos=None, color="steelblue", es_pct=False):
    """
    Genera un gráfico de barras para una métrica por segmento de renta del municipio.

    Parameters
    ----------
    serie : pd.Series
        Serie de Pandas con los datos a graficar. El índice representa los segmentos.
    titulo : str
        Título principal del gráfico.
    etiqueta_y : str
        Etiqueta para el eje vertical (Y).
    orden_segmentos : list, optional
        Lista con el orden específico en el que se deben mostrar los segmentos (ej. ORDEN_SEG).
        Si es None, se mantendrá el orden original de la serie.
    color : str, default "steelblue"
        Color de las barras del gráfico.
    es_pct : bool, default False
        Si es True, da formato de porcentaje (%.1f%%) a las etiquetas de las barras.
        Si es False, usa formato decimal simple (%.1f).
    """
    # Si se proporciona un orden específico, reindexamos la serie de forma segura
    if orden_segmentos is not None:
        # Filtramos el orden para incluir solo los segmentos que realmente existan en la serie
        orden_valido = [seg for seg in orden_segmentos if seg in serie.index]
        serie = serie.reindex(orden_valido)
    
    fig, ax = plt.subplots()
    
    # Dibujamos las barras convirtiendo el índice a string para evitar problemas de formato
    barras = ax.bar(serie.index.astype(str), serie.values, color=color)
    
    # Añadimos los valores encima de cada barra
    ax.bar_label(barras, fmt="%.1f%%" if es_pct else "%.1f", padding=3)
    
    # Configuramos textos y etiquetas
    ax.set_title(titulo)
    ax.set_ylabel(etiqueta_y)
    ax.set_xlabel("Segmento de renta del municipio")
    
    # Añadimos un pequeño margen superior para que las etiquetas de las barras no se corten
    ax.margins(y=0.15)
    
    fig.tight_layout()
    plt.show()


def barras_comparacion_segmento(serie_a, serie_b, etiqueta_a, etiqueta_b, titulo,
                                etiqueta_y, orden_segmentos=None,
                                color_a="seagreen", color_b="darkorange", es_pct=False):
    """
    Compara una misma métrica en dos subconjuntos, por segmento de renta, con
    barras agrupadas (dos barras por segmento).
 
    Pensada para mostrar si un gradiente se mantiene al excluir un subgrupo: por
    ejemplo, el % de electrificados por renta calculado sobre TODOS los coches
    frente al calculado SOLO sobre los que NO son de renting (control de H5).
 
    Parameters
    ----------
    serie_a, serie_b : pd.Series
        Series a comparar lado a lado. Comparten el mismo índice de segmentos.
    etiqueta_a, etiqueta_b : str
        Nombres de cada serie para la leyenda.
    titulo : str
        Título principal del gráfico.
    etiqueta_y : str
        Etiqueta del eje vertical (Y).
    orden_segmentos : list, optional
        Orden en el que mostrar los segmentos (ej. ORDEN_SEG). Si es None, usa el
        orden de 'serie_a'. Solo se muestran los segmentos presentes en serie_a.
    color_a, color_b : str
        Colores de cada grupo de barras.
    es_pct : bool, default False
        Si es True, da formato de porcentaje (%.1f%%) a las etiquetas.
    """
    # Reindexamos ambas series al mismo orden de segmentos, de forma segura
    if orden_segmentos is not None:
        orden_valido = [seg for seg in orden_segmentos if seg in serie_a.index]
    else:
        orden_valido = list(serie_a.index)
    serie_a = serie_a.reindex(orden_valido)
    serie_b = serie_b.reindex(orden_valido)
 
    x = np.arange(len(orden_valido))
    ancho = 0.38
 
    fig, ax = plt.subplots()
    barras_a = ax.bar(x - ancho / 2, serie_a.values, ancho, label=etiqueta_a, color=color_a)
    barras_b = ax.bar(x + ancho / 2, serie_b.values, ancho, label=etiqueta_b, color=color_b)
 
    fmt = "%.1f%%" if es_pct else "%.1f"
    ax.bar_label(barras_a, fmt=fmt, padding=2, fontsize=8)
    ax.bar_label(barras_b, fmt=fmt, padding=2, fontsize=8)
 
    ax.set_xticks(x)
    ax.set_xticklabels([str(seg) for seg in orden_valido])
    ax.set_title(titulo)
    ax.set_ylabel(etiqueta_y)
    ax.set_xlabel("Segmento de renta del municipio")
    ax.legend()
    ax.margins(y=0.15)
 
    fig.tight_layout()
    plt.show()    


def dispersion_municipio(df_muni, x, y, titulo, etiqueta_x, etiqueta_y, color="seagreen"):
    """
    Dibuja un grafico de dispersion a nivel municipio (un punto por municipio) para
    mostrar la relacion CONTINUA entre dos variables, normalmente la renta frente a
    una metrica del parque. Sirve como control de la discretizacion en quintiles: si
    la nube se inclina en la misma direccion que el gradiente por segmentos, el patron
    no es un artefacto de donde se trazaron las fronteras de los grupos.

    Parameters
    ----------
    df_muni : pd.DataFrame
        Tabla agregada a nivel municipio (un registro por municipio).
    x, y : str
        Nombres de las columnas para los ejes X e Y.
    titulo : str
        Titulo principal del grafico.
    etiqueta_x, etiqueta_y : str
        Etiquetas de los ejes X e Y.
    color : str, default "seagreen"
        Color de los puntos.
    """
    fig, ax = plt.subplots()
    ax.scatter(df_muni[x], df_muni[y], s=18, alpha=0.5, color=color)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    fig.tight_layout()
    plt.show()    