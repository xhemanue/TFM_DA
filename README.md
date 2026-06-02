# TFM — Análisis del Parque de Vehículos vs. Renta de los Hogares

> Trabajo Fin de Máster · Data Analytics
> Pipeline end-to-end: ingesta → limpieza → EDA → dashboard.

---

## 1. Resumen del proyecto

*(Pendiente de redactar)* — Descripción breve del objetivo, las fuentes y la pregunta
analítica principal: relación entre la composición del parque de turismos y el nivel de
renta del territorio, a nivel municipal, en las 5 provincias con mayor parque de España.

## 2. Fuentes de datos

| Fuente | Descripción | Periodo | Origen |
|---|---|---|---|
| DGT — Microdatos parque de vehículos | Censo de vehículos matriculados | Marzo 2026 | Datos abiertos DGT |
| INE — Atlas de Distribución de Renta | Indicadores de renta por municipio | 2023 | INEbase |
| INE — Códigos de provincia | Tabla maestra código↔nombre | — | INEbase |

> **Nota sobre el desfase temporal.** *(Pendiente — desarrollar aquí la justificación
> completa: parque 2026 vs renta 2023, validez por baja volatilidad de la renta
> municipal, salvedad de municipios de cambio rápido.)*

## 3. Estructura del repositorio

```
TFM/
├── data/
│   ├── raw/          Fuentes originales (intocables)
│   └── processed/    Datasets generados por el pipeline (Parquet)
├── notebooks/        Notebooks numerados por fase
├── src/              Funciones reutilizables (tfm_io, tfm_limpieza, tfm_eda)
├── dashboard/        Cuadro de mando (.pbix)
├── reports/          Informe ejecutivo
├── requirements.txt  Dependencias
└── README.md
```

## 4. Fases del pipeline

1. **Adquisición e integración** (`01_adquisicion_integracion.ipynb`) — descarga,
   filtrado y fusión DGT↔INE por código de municipio.
2. **Limpieza / ETL** (`02_limpieza_etl.ipynb`) — nulos, tipos, estandarización,
   feature engineering.
3. **EDA** (`03_eda.ipynb`) — perfilado, distribuciones, outliers, correlaciones.
4. **Análisis estadístico** (`04_analisis_estadistico.ipynb`).
5. **Dashboard** (`dashboard/`) e **informe** (`reports/`).

## 5. Cómo reproducir

```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Colocar las fuentes en data/raw/ (ver sección 2 para el origen)
# 4. Ejecutar los notebooks en orden (01 → 04)
```

## 6. Conclusiones

*(Pendiente — resumen de los insights principales del análisis.)*

---

*Decisiones metodológicas detalladas (selección de 5 provincias, formato Parquet,
tratamiento de nulos, desfase temporal entre fuentes) documentadas en sus secciones
correspondientes.*
