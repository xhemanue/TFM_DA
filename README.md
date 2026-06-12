# TFM — Análisis del Parque de Vehículos vs. Renta de los Hogares

> Trabajo Fin de Máster · Data Analytics
> Proceso completo de datos: adquisición → limpieza → EDA → análisis descriptivo → dashboard → informe.

## Contexto académico

Este proyecto constituye el Trabajo Fin de Máster del programa de Data Analytics.
Consiste en desarrollar un proceso completo de datos sobre un caso de
análisis libre, partiendo de cero, que demuestre el dominio de la adquisición, la limpieza, la fusión multifuente, el análisis estadístico y la visualización de datos.

### Requisitos y cumplimiento

| **Requisito** | **Cómo lo cumple este proyecto** |
| :--- | :--- |
| Mínimo 2 fuentes en bruto, de canales distintos | DGT (microdatos del parque) + INE (Atlas de Renta) |
| Fusión mediante llave común | Código INE de municipio (5 dígitos) |
| Mínimo 50.000 filas y 20 columnas tras la fusión | Dataset fusionado: **6.613.034 filas × 54 columnas** |
| Dataset final limpio y enriquecido | Dataset procesado: **6.613.034 filas × 37 columnas** |
| Variables numéricas, categóricas y temporales | Presentes (potencia, marca, fecha de matriculación, etc.) |
| Pipeline completo: ETL → EDA → dashboard → informe | Notebooks por fase + dashboard + informe |
| Tecnologías: Python/Pandas, Power BI, GitHub | Empleadas según se exige |

---

## 1. Resumen del proyecto

El proyecto estudia la relación entre el **nivel de renta de un territorio** y el **perfil del parque de turismos** que circula en él (potencia, cilindrada, antigüedad, marca, tipo de propulsión y electrificación), a nivel **municipal**, en las **5 provincias con mayor parque de España** (Madrid, Barcelona, Valencia, Alicante y Sevilla).

**Pregunta analítica central:** ¿existe relación entre la renta municipal y las características del parque de vehículos que se domicilia en ese municipio?

**Hipótesis de trabajo:**

* **H1** — A mayor renta municipal, mayor potencia y cilindrada medias.
* **H2** — A mayor renta municipal, menor antigüedad media del parque.
* **H3** — La penetración de vehículos electrificados (BEV/PHEV/HEV) crece con la renta.
- **H4** — Las marcas de gama alta se concentran en municipios de renta alta.
- **H5** — El renting introduce un sesgo (vehículos más nuevos/potentes) que puede actuar como variable de confusión.

> La gama de marca (H4) se trata como **resultado emergente** del cruce marca↔renta, no como una etiqueta *premium* asignada a priori (ver §4, "Decisión sobre la gama").

## 2. Fuentes de datos

| **Fuente** | **Descripción** | **Periodo** | **Origen** |
| :--- | :--- | :--- | :--- |
| DGT — Microdatos del parque de vehículos | Censo de vehículos vigentes, un registro por vehículo | Marzo 2026 | Datos abiertos DGT (*DGT en cifras*) |
| INE — Atlas de Distribución de Renta de los Hogares | Indicadores de renta por municipio | 2023 | INEbase |
| INE — Códigos de provincia | Tabla maestra código↔nombre | — | INEbase |

**Documentación de respaldo.** El campo y los códigos del fichero DGT están definidos en el documento oficial *Interfaz de salida — Fichero de Parque Anual* (ONSV/DGT), incluido en `data/raw/` como referencia. De él se han tomado los diccionarios de `PROPULSION`, `CATELECT`, `ALIMENTACION`, `PROCEDENCIA`, `RENTING`, etc., y la documentación de las reglas de anonimización de la fuente.

## 3. Estructura del repositorio

```
TFM_DA/
├── data/
│   ├── raw/          Fuentes originales intocables + documentación oficial
│   │   ├── parque_vehiculos_202603.txt
│   │   ├── 30824.csv
│   │   ├── codprov.xls
│   │   ├── Interfaz-de-Salida-Fichero-Parque-Anual.pdf   (diccionario oficial DGT)
│   │   └── LEEME_fuentes.md
│   └── processed/    Datasets generados por el pipeline
│       ├── dgt_top5_turismos_2010_202603.parquet   (subconjunto DGT)
│       ├── dataset_fusionado.parquet               (salida Fase 0)
│       ├── dataset_procesado.parquet               (salida Fase 1, dataset final)
│       └── powerbi_*.csv / .parquet               (tablas de hechos y dimensiones para Power BI, Fase 3)
├── notebooks/
│   ├── 01_adquisicion_integracion.ipynb
│   ├── 02_limpieza_etl.ipynb
│   ├── 03_eda.ipynb
│   └── 04_analisis_estadistico.ipynb
├── src/              Funciones reutilizables
│   ├── tfm_io.py        (carga/guardado de fuentes, export CSV/Parquet)
│   ├── tfm_limpieza.py  (estandarización, nulos)
│   ├── tfm_eda.py       (perfilado y EDA)
│   └── tfm_vis.py       (gráficos: barras por segmento y dispersión)
├── dashboard/        
│   └── tfm_da.pbix       (Cuadro de mando - PowerBI)
├── reports/         
│   └── Informe_Analisis_TFM.md       (Informe del análisis de datos)
├── requirements.txt
└── README.md
```

## 4. Decisiones metodológicas

**Selección de 5 provincias.** Madrid, Barcelona, Valencia, Alicante y Sevilla concentran el **38,81 %** del parque nacional de turismos (10.088.758 de 25.994.390). La elección se justifica con datos por peso en el parque, diversidad de perfiles territoriales y viabilidad computacional.

**Corte temporal en 2010.** Solo se incluyen vehículos matriculados desde 2010. En consecuencia, la variable `antiguedad` está acotada a \~16 años; las conclusiones se refieren al "parque matriculado desde 2010", no al parque histórico completo.

**Desfase temporal entre fuentes.** El parque DGT es de marzo 2026 y la renta INE de 2023 (último año publicado; el INE va con \~2 años de retardo por usar datos fiscales consolidados). El cruce es válido porque la renta municipal es **estructural y de baja volatilidad**; la salvedad son municipios de cambio socioeconómico muy rápido, poco frecuentes en el horizonte considerado.

**Formato Parquet.** Los datasets intermedios y finales se guardan en Parquet (frente a CSV: \~5–10× menos espacio, conserva los tipos y carga más rápido), decisión justificada por el volumen (varios millones de filas).

**Cobertura municipal (limitación documentada).** Según la interfaz oficial de la DGT, la variable `MUNICIPIO` se **suprime** para los vehículos domiciliados en municipios de **menos de 10.000 habitantes** (anonimización). Por ello, el \~16,79 % de vehículos sin municipio (\~1,1 M) corresponde a municipios pequeños, no a un error de datos. **El análisis renta↔parque queda acotado a los 273 municipios de ≥10.000 habitantes** presentes en el cruce; no es generalizable al ámbito rural. Se gestiona con la bandera `tiene_municipio` y el segmento `"SIN DATO"`.

**Anonimización de marca/modelo.** La DGT enmascara con el carácter `¡` (tratado como `NA`) los valores de `MARCA`/`MODELO` con ≤5 ocurrencias. Los nulos de estas columnas no son datos perdidos sino valores raros enmascarados; se etiquetan como `"DESCONOCIDO"`.

**Gestión de nulos sin imputación artificial.** No se imputan medias ni modas: la renta se conserva como `NaN` donde no hay municipio (imputarla sería inventar el dato), las categóricas descriptivas reciben el nivel `"DESCONOCIDO"`, y las métricas ambientales conservan su `NaN`.

**Tratamiento de valores atípicos de motor (en el EDA).** El saneado de motor se hace en el EDA (Fase 2), no en el ETL, porque requería *ver* las distribuciones: el *placeholder* `kw ≈ 999.99`, los ceros imposibles (`cilindrada = 0` en combustión y `kw = 0`) y un tope de potencia de **800 kW** (\~1.090 CV, por encima del cual no existen turismos de producción) se marcan como `NaN` y se recalcula `potencia_cv`. El tope se justifica con un diagnóstico de la cola alta: deportivos reales hasta \~600 kW frente a un "montón" artificial de \~330 coches por encima.

**Interpretación de `consumo` y `autonomia`.** Según el documento oficial, son métricas **eléctricas** (consumo Wh/km y autonomía eléctrica en km, WLTP), no consumo de combustible. Solo tienen valor en electrificados. La métrica ambiental transversal a todos los vehículos es `emisiones_co2` (g/km, WLTP).

**Enfoque descriptivo (censo, no muestra).** El dataset es prácticamente un censo del parque (están todos los turismos, no una selección). Con la población completa, la estadística descriptiva (medias, medianas y porcentajes por nivel de renta) describe directamente la realidad, así que el análisis **no usa tests de inferencia ni modelos predictivos**: se mantiene en un nivel descriptivo, riguroso y plenamente justificable.

**Segmentación por quintiles y validación continua.** La renta municipal se discretiza en cinco quintiles (`Muy baja` → `Muy alta`) como lente para comparar perfiles. Para descartar que el gradiente dependa de dónde se trazan las fronteras de los grupos, se valida con una **vista continua**: una dispersión a nivel municipio (un punto por municipio) de la renta frente a la métrica, que confirma la misma tendencia sin discretizar.

**Decisión sobre la gama (no se crea `premium`).** No se crea una variable booleana *premium*: "premium" es una segmentación comercial subjetiva, y definirla por atributos técnicos (potencia/cilindrada) generaría **circularidad** con H1. La gama se analiza como patrón emergente del cruce marca↔renta.

**Vectorización y memoria.** Todas las transformaciones son vectorizadas (sin bucles fila a fila ni `apply`/`lambda` sobre los 6,6 M de registros): se usan `.str`, `.map(dict)`, `.replace`, `np.where`, `pd.qcut` y aritmética nativa, y para texto en categóricas se opera sobre las categorías, no sobre las filas. Los tipos se optimizan con `category`, `Int8/16` y `float32`. La carga de ficheros se protege con `try/except`.

## 5. Variables del dataset final (`dataset_procesado.parquet`, 37 columnas)

| **Grupo** | **Variables** |
| :--- | :--- |
| Territorio | `provincia`, `nombre_provincia`, `municipio`, `cod_municipio`, `nombre_municipio`, `tiene_municipio`, `segmento_renta` |
| Renta (INE) | `renta_media_uc`, `renta_mediana_uc`, `renta_bruta_hogar`, `renta_bruta_persona`, `renta_neta_hogar`, `renta_neta_persona` |
| Identificación | `marca`, `modelo` |
| Matriculación / antigüedad | `fec_prim_matr`, `anio_matriculacion`, `antiguedad`, `procedencia`, `nuevo_usado` |
| Titularidad / negocio | `tipo_titular`, `num_titulares`, `renting` |
| Prestaciones | `cilindrada`, `kw`, `potencia_cv` |
| Combustible / electrificación | `tipo_combustible`, `es_electrificado`, `tipo_electrificacion`, `alimentacion` |
| Ambiental | `consumo`, `autonomia`, `emisiones_co2`, `tipo_distintivo`, `emisiones_euro` |
| Clasificación | `cat_euro`, `carroceria` |

Variables derivadas en el *feature engineering*: `anio_matriculacion`, `antiguedad`, `potencia_cv`, `tipo_combustible`, `es_electrificado`, `tipo_electrificacion`, `segmento_renta`.

## 6. Fases del pipeline

| **Fase** | **Entregable** | **Estado** |
| :--- | :--- | :--- |
| 0. Adquisición e integración | `01_adquisicion_integracion.ipynb` | ✅ Completada |
| 1. Limpieza / ETL + Feature Engineering | `02_limpieza_etl.ipynb` | ✅ Completada |
| 2. EDA | `03_eda.ipynb` | ✅ Completada |
| 3. Análisis estadístico descriptivo | `04_analisis_estadistico.ipynb` | ✅ Completada |
| 4. Dashboard (Power BI) | `dashboard/tfm_da.pbix` | ✅ Completada |
| 5. Informe del análisis | `reports/Informe_Analisis_TFM.md` | ✅ Completada |

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
#    03_eda.ipynb                      -> exploración y limpieza (no genera datos)
#    04_analisis_estadistico.ipynb     -> análisis descriptivo + tablas powerbi_*.csv
```

> Los ficheros de datos pesados no se versionan en GitHub (el subconjunto DGT supera el límite de 100 MB). Se regeneran ejecutando los notebooks sobre las fuentes originales descritas en `data/raw/LEEME_fuentes.md`.

## 8. Conclusiones

Conclusiones del análisis descriptivo. El parque completo de las 5 provincias es de 6.613.034 turismos; el análisis renta↔parque se realiza sobre los **5.502.832 vehículos** domiciliados en los **273 municipios de ≥10.000 habitantes** con renta del INE disponible (ver §4, "Cobertura municipal"). Al trabajar con la población completa (no una muestra), las medias, medianas y porcentajes por nivel de renta describen directamente la realidad, sin necesidad de inferencia estadística.

**Resumen descriptivo de las hipótesis:**

| **Hipótesis** | **Hallazgo descriptivo (Fase 3)** | **Interpretación** |
| :--- | :--- | :--- |
| **H1** Potencia/cilindrada ↑ con renta | Potencia media \~121→131 CV (sube leve); cilindrada casi plana \~1.480–1.490 cc | Se cumple a medias (potencia sí, cilindrada no) |
| **H2** Antigüedad ↓ con renta | Media de \~8,5 años (renta muy baja) → \~6,3 años (renta muy alta) | **Se observa con claridad** |
| **H3** Electrificación ↑ con renta | % de electrificados: \~12,7% (muy baja) → \~31,4% (muy alta); penetración global \~24% | **Tendencia muy marcada** |
| **H4** Marcas de gama alta ↑ con renta | % de gama alta: \~15,1% (muy baja) → \~19,5% (muy alta); Audi aparece en top8 de "muy alta" | Tendencia **leve**, emergente |
| **H5** Renting confunde | Renting: antigüedad \~2,0 años vs. resto \~7,5; potencia \~135 vs. \~126 CV; electrificados \~50% vs. \~21,5% | **Sesgo marcado** requiere control |

**Colinealidad detectada en el EDA:** dos bloques de variables casi redundantes.

* Bloque motor: `kw`–`cilindrada`–`potencia_cv` (correlación kw/potencia_cv = 1,00 por construcción).
* Bloque renta: las 6 variables del INE (correlación 0,96–1,00 entre sí).

Por eso el análisis usa un único representante de cada bloque (`potencia_cv` y `renta_neta_persona`), y en el dashboard basta con una variable de renta.

**Valor del análisis:**

* A mayor renta, el parque es más **nuevo** y más **electrificado** (efectos claros).
* La **potencia** sube con la renta pero de forma leve; la **cilindrada** es casi invariante.
* El **renting** introduce sesgo significativo: hay que controlarlo en H2 y H3.
* El **patrón de marcas** (gama alta concentrada en renta alta) existe pero es débil e ilustrativo, no una etiqueta binaria.

**Entregables finales:** el cuadro de mando interactivo en Power BI (`dashboard/tfm_da.pbix`), que permite segmentar los resultados por provincia, año y nivel de renta, y el informe del análisis (`reports/Informe_Analisis_TFM.md`), que recoge y discute los hallazgos.
