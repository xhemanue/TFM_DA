# TFM — Análisis del Parque de Vehículos vs. Renta de los Hogares

> Trabajo Fin de Máster · Data Analytics
> Pipeline end-to-end: ingesta → limpieza → EDA → dashboard → informe.

## Contexto académico

Este proyecto constituye el Trabajo Fin de Máster del programa de Data Analytics.
Consiste en desarrollar un pipeline de datos de extremo a extremo sobre un caso de
análisis libre, partiendo de cero, que demuestre el dominio de la ingesta, la limpieza
profunda, la fusión multifuente, el análisis estadístico y la visualización de datos.

### Requisitos y cumplimiento

| Requisito | Cómo lo cumple este proyecto |
|---|---|
| Mínimo 2 fuentes en bruto, de canales distintos | DGT (microdatos del parque) + INE (Atlas de Renta) |
| Fusión mediante llave común | Código INE de municipio (5 dígitos) |
| Mínimo 50.000 filas y 20 columnas tras la fusión | Dataset fusionado: **6.613.034 filas × 54 columnas** |
| Dataset final limpio y enriquecido | Dataset procesado: **6.613.034 filas × 37 columnas** |
| Variables numéricas, categóricas y temporales | Presentes (potencia, marca, fecha de matriculación, etc.) |
| Pipeline completo: ETL → EDA → dashboard → informe | Notebooks por fase + dashboard + informe |
| Tecnologías: Python/Pandas, Power BI, GitHub | Empleadas según se exige |

---

## 1. Resumen del proyecto

El proyecto estudia la relación entre el **nivel de renta de un territorio** y el
**perfil del parque de turismos** que circula en él (potencia, cilindrada, antigüedad,
marca, tipo de propulsión y electrificación), a nivel **municipal**, en las **5 provincias
con mayor parque de España** (Madrid, Barcelona, Valencia, Alicante y Sevilla).

**Pregunta analítica central:** ¿existe relación entre la renta municipal y las
características del parque de vehículos que se domicilia en ese municipio?

**Hipótesis de trabajo:**

- **H1** — A mayor renta municipal, mayor potencia y cilindrada medias.
- **H2** — A mayor renta municipal, menor antigüedad media del parque.
- **H3** — La penetración de vehículos electrificados (BEV/PHEV/HEV) crece con la renta.
- **H4** — Las marcas de gama alta se concentran en municipios de renta alta.
- **H5** — El renting introduce un sesgo (vehículos más nuevos/potentes) que puede actuar
  como variable de confusión.

> La gama de marca (H4) se trata como **resultado emergente** del cruce marca↔renta, no
> como una etiqueta *premium* asignada a priori (ver §4, "Decisión sobre la gama").

## 2. Fuentes de datos

| Fuente | Descripción | Periodo | Origen |
|---|---|---|---|
| DGT — Microdatos del parque de vehículos | Censo de vehículos vigentes, un registro por vehículo | Marzo 2026 | Datos abiertos DGT (*DGT en cifras*) |
| INE — Atlas de Distribución de Renta de los Hogares | Indicadores de renta por municipio | 2023 | INEbase |
| INE — Códigos de provincia | Tabla maestra código↔nombre | — | INEbase |

**Documentación de respaldo.** El campo y los códigos del fichero DGT están definidos en
el documento oficial *Interfaz de salida — Fichero de Parque Anual* (ONSV/DGT), incluido
en `data/raw/` como referencia. De él se han tomado los diccionarios de `PROPULSION`,
`CATELECT`, `ALIMENTACION`, `PROCEDENCIA`, `RENTING`, etc., y la documentación de las
reglas de anonimización de la fuente.

## 3. Estructura del repositorio

```
TFM_DA/
├── data/
│   ├── raw/          Fuentes originales intocables + documentación oficial
│   │   ├── parque_vehiculos_202603.txt
│   │   ├── 30824.csv
│   │   ├── codprov.xls
│   │   └── LEEME_fuentes.md
│   └── processed/    Datasets generados por el pipeline (Parquet)
│       ├── dgt_top5_turismos_2010_202603.parquet   (subconjunto DGT)
│       ├── dataset_fusionado.parquet               (salida Fase 0)
│       └── dataset_procesado.parquet               (salida Fase 1, dataset final)
├── notebooks/
│   ├── 01_adquisicion_integracion.ipynb
│   └── 02_limpieza_etl.ipynb
├── src/              Funciones reutilizables
│   ├── tfm_io.py        (carga/guardado de fuentes)
│   ├── tfm_limpieza.py  (estandarización, nulos)
│   └── tfm_eda.py       (perfilado y EDA)
├── dashboard/        Cuadro de mando (.pbix)
├── reports/          Informe ejecutivo
├── requirements.txt
└── README.md
```

## 4. Decisiones metodológicas

**Selección de 5 provincias.** Madrid, Barcelona, Valencia, Alicante y Sevilla concentran
el **38,81 %** del parque nacional de turismos (10.088.758 de 25.994.390). La elección se
justifica con datos por peso en el parque, diversidad de perfiles territoriales y
viabilidad computacional.

**Corte temporal en 2010.** Solo se incluyen vehículos matriculados desde 2010. En
consecuencia, la variable `antiguedad` está acotada a ~16 años; las conclusiones se
refieren al "parque matriculado desde 2010", no al parque histórico completo.

**Desfase temporal entre fuentes.** El parque DGT es de marzo 2026 y la renta INE de 2023
(último año publicado; el INE va con ~2 años de retardo por usar datos fiscales
consolidados). El cruce es válido porque la renta municipal es **estructural y de baja
volatilidad**; la salvedad son municipios de cambio socioeconómico muy rápido, poco
frecuentes en el horizonte considerado.

**Formato Parquet.** Los datasets intermedios y finales se guardan en Parquet (frente a
CSV: ~5–10× menos espacio, conserva los tipos y carga más rápido), decisión justificada
por el volumen (varios millones de filas).

**Cobertura municipal (limitación documentada).** Según la interfaz oficial de la DGT, la
variable `MUNICIPIO` se **suprime** para los vehículos domiciliados en municipios de
**menos de 10.000 habitantes** (anonimización). Por ello, el ~16,79 % de vehículos sin
municipio (~1,1 M) corresponde a municipios pequeños, no a un error de datos. **El análisis
renta↔parque queda acotado a los 273 municipios de ≥10.000 habitantes** presentes en el
cruce; no es generalizable al ámbito rural. Se gestiona con la bandera `tiene_municipio` y
el segmento `"SIN DATO"`.

**Anonimización de marca/modelo.** La DGT enmascara con el carácter `¡` (tratado como `NA`)
los valores de `MARCA`/`MODELO` con ≤5 ocurrencias. Los nulos de estas columnas no son
datos perdidos sino valores raros enmascarados; se etiquetan como `"DESCONOCIDO"`.

**Gestión de nulos sin imputación artificial.** No se imputan medias ni modas: la renta se
conserva como `NaN` donde no hay municipio (imputarla sería inventar el dato), las
categóricas descriptivas reciben el nivel `"DESCONOCIDO"`, y las métricas ambientales
conservan su `NaN`.

**Interpretación de `consumo` y `autonomia`.** Según el documento oficial, son métricas
**eléctricas** (consumo Wh/km y autonomía eléctrica en km, WLTP), no consumo de
combustible. Solo tienen valor en electrificados. La métrica ambiental transversal a todos
los vehículos es `emisiones_co2` (g/km, WLTP).

**Decisión sobre la gama (no se crea `premium`).** No se crea una variable booleana
*premium*: "premium" es una segmentación comercial subjetiva, y definirla por atributos
técnicos (potencia/cilindrada) generaría **circularidad** con H1. La gama se analiza como
patrón emergente del cruce marca↔renta.

**Vectorización y memoria.** Todas las transformaciones son vectorizadas (sin bucles fila a
fila ni `apply`/`lambda` sobre los 6,6 M de registros): se usan `.str`, `.map(dict)`,
`.replace`, `np.where`, `pd.qcut` y aritmética nativa, y para texto en categóricas se opera
sobre las categorías, no sobre las filas. Los tipos se optimizan con `category`, `Int8/16`
y `float32`. La carga de ficheros se protege con `try/except`.

## 5. Variables del dataset final (`dataset_procesado.parquet`, 37 columnas)

| Grupo | Variables |
|---|---|
| Territorio | `provincia`, `nombre_provincia`, `municipio`, `cod_municipio`, `nombre_municipio`, `tiene_municipio`, `segmento_renta` |
| Renta (INE) | `renta_media_uc`, `renta_mediana_uc`, `renta_bruta_hogar`, `renta_bruta_persona`, `renta_neta_hogar`, `renta_neta_persona` |
| Identificación | `marca`, `modelo` |
| Matriculación / antigüedad | `fec_prim_matr`, `anio_matriculacion`, `antiguedad`, `procedencia`, `nuevo_usado` |
| Titularidad / negocio | `tipo_titular`, `num_titulares`, `renting` |
| Prestaciones | `cilindrada`, `kw`, `potencia_cv` |
| Combustible / electrificación | `tipo_combustible`, `es_electrificado`, `tipo_electrificacion`, `alimentacion` |
| Ambiental | `consumo`, `autonomia`, `emisiones_co2`, `tipo_distintivo`, `emisiones_euro` |
| Clasificación | `cat_euro`, `carroceria` |

Variables derivadas en el *feature engineering*: `anio_matriculacion`, `antiguedad`,
`potencia_cv`, `tipo_combustible`, `es_electrificado`, `tipo_electrificacion`,
`segmento_renta`.

## 6. Fases del pipeline

| Fase | Entregable | Estado |
|---|---|---|
| 0. Adquisición e integración | `01_adquisicion_integracion.ipynb` | ✅ Completada |
| 1. Limpieza / ETL + Feature Engineering | `02_limpieza_etl.ipynb` | ✅ Completada |
| 2. EDA | `03_eda.ipynb` | ⏳ Pendiente |
| 3. Análisis estadístico | `04_analisis_estadistico.ipynb` | ⏳ Pendiente |
| 4. Dashboard | `dashboard/*.pbix` | ⏳ Pendiente |
| 5. Informe ejecutivo | `reports/` | ⏳ Pendiente |

## 7. Cómo reproducir

```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Colocar las fuentes en data/raw/ (ver §2 para el origen)
# 4. Ejecutar los notebooks en orden:
#    01_adquisicion_integracion.ipynb  -> genera dataset_fusionado.parquet
#    02_limpieza_etl.ipynb             -> genera dataset_procesado.parquet
```

> Los ficheros de datos pesados no se versionan en GitHub (el subconjunto DGT supera el
> límite de 100 MB). Se regeneran ejecutando los notebooks sobre las fuentes originales
> descritas en `data/raw/LEEME_fuentes.md`.

## 8. Conclusiones

*(Pendiente — se desarrollará tras el EDA y el análisis estadístico: validación de las
hipótesis H1–H5, traducción de las métricas en insights de negocio y recomendaciones
accionables. Se incluirá la discusión de la colinealidad entre variables cuantitativas
—p. ej. `kw`–`cilindrada` y las 6 variables de renta entre sí— y su impacto de cara a un
eventual modelo predictivo.)*