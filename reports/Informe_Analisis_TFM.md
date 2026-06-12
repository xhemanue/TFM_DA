# Informe del análisis de datos

## Relación entre la renta de los hogares y el perfil del parque de turismos
**Trabajo Fin de Máster · Data Analytics** *Fuentes: DGT (parque de vehículos, marzo de 2026) e INE (Atlas de Renta, 2023). Junio de 2026.*

---

### Resumen
Este informe recoge los resultados del análisis descriptivo de la relación entre la renta de los hogares, a nivel municipal, y el perfil del parque de turismos en las cinco provincias españolas con mayor parque nacional (Madrid, Barcelona, Valencia, Alicante y Sevilla). Sobre un conjunto de 5.502.832 vehículos correspondientes a 273 municipios, se contrastan cinco hipótesis relativas a la potencia, la antigüedad, la electrificación, la presencia de marcas de gama alta y el papel del renting. Se observa un gradiente claro de la antigüedad y de la electrificación con la renta, un efecto leve en la potencia y escaso en la gama alta, y un sesgo apreciable —aunque no determinante— asociado al renting.

---

### 1. Introducción y objetivo
El objetivo del trabajo es estudiar si existe relación entre el nivel de renta de un municipio y las características del parque de turismos domiciliado en él: potencia, cilindrada, antigüedad, marca, propulsión y grado de electrificación.

La pregunta se concreta en cinco hipótesis. A mayor renta municipal:
* **(H1)** Mayor potencia y cilindrada medias.
* **(H2)** Menor antigüedad del parque.
* **(H3)** Mayor proporción de vehículos electrificados.
* **(H4)** Mayor presencia de marcas de gama alta.
* **(H5)** Plantea que el renting, al concentrar vehículos más nuevos y electrificados, puede actuar como factor de confusión que conviene controlar.

### 2. Datos y metodología
Se emplean dos fuentes de datos abiertos: los microdatos del parque de vehículos de la DGT (marzo de 2026) y el Atlas de Distribución de Renta de los Hogares del INE (2023), unidos por el código INE de municipio de cinco dígitos. El alcance se limita a las cinco provincias indicadas, que concentran el 38,8 % del parque nacional de turismos, y a los vehículos matriculados desde 2010.

El análisis renta–parque se realiza sobre los 5.502.832 vehículos de los 273 municipios de 10.000 o más habitantes para los que el INE publica renta. La DGT suprime el municipio en poblaciones menores por anonimización, de modo que esos vehículos no pueden cruzarse con la renta y quedan fuera de esta parte del análisis.

El tratamiento es descriptivo. Al trabajar sobre la población completa —un censo, no una muestra—, las medias, medianas y porcentajes por nivel de renta describen directamente la realidad observada, por lo que no se recurre a contrastes de inferencia. La renta se agrupa en cinco quintiles calculados a nivel de municipio (no de vehículo), de manera que cada tramo reúne una quinta parte de los municipios; los promedios por encima del municipio se ponderan por el número de vehículos.

### 3. Resultados

#### 3.1. Contraste de las hipótesis
La tabla siguiente recoge el contraste de las cinco hipótesis por nivel de renta del municipio.

| Hipótesis | Resultado (cifras) | Lectura |
| :--- | :--- | :--- |
| **H1 — Potencia / cilindrada** | Potencia media 121,3 → 130,8 CV (+7,8 %). Cilindrada casi constante (~1.480–1.500 cc). | Se cumple parcialmente: la potencia sube de forma leve; la cilindrada apenas varía. |
| **H2 — Antigüedad** | 8,5 años (renta muy baja) → 6,3 años (renta muy alta): −2,2 años. | Se confirma con claridad: a mayor renta, parque más nuevo. |
| **H3 — Electrificación** | 12,7 % → 31,4 % de electrificados (×2,5). Media del conjunto ~24 %. | Es el gradiente más marcado del estudio. |
| **H4 — Marcas de gama alta** | 15,1 % → 19,5 % (+4,4 puntos). | Tendencia leve; se interpreta como patrón emergente. |
| **H5 — Renting (confusión)** | Renting frente al resto: antigüedad 2,0 vs 7,5 años; electrificados 50,1 % vs 21,5 %. | Sesga el parque, pero al aislarlo el gradiente de renta se mantiene. |

#### 3.2. Composición del parque por combustible
El parque continúa dominado por la gasolina (57,8 %) y el diésel (37,0 %). El vehículo puramente eléctrico es todavía minoritario (3,0 %); la cifra de vehículos electrificados (en torno al 24 %) procede en su mayor parte de los híbridos. Conviene tenerlo presente al interpretar H3: lo que aumenta con la renta es, sobre todo, la hibridación, mientras que el eléctrico puro se encuentra aún en una fase inicial.

#### 3.3. El renting como factor de confusión
El renting representa alrededor del 12 % del parque y concentra vehículos sensiblemente más nuevos (2,0 frente a 7,5 años de media) y más electrificados (50,1 % frente a 21,5 %). Para comprobar si el gradiente de renta es un reflejo de la distribución del renting, se repitió el análisis únicamente sobre los vehículos que no son de renting: la electrificación sigue creciendo con la renta (del 12,9 % al 27,4 %) y la antigüedad sigue descendiendo. El renting acentúa el patrón, pero no lo origina.

#### 3.4. Comprobaciones de robustez
El mismo orden se observa entre provincias: la proporción de electrificados sigue el nivel de renta, con Madrid en el extremo superior y Sevilla en el inferior.

| Provincia | Vehículos analizados | % electrificados |
| :--- | :--- | :--- |
| **Madrid** | 2.561.957 | 31,0 % |
| **Barcelona** | 1.294.219 | 20,2 % |
| **Valencia** | 627.621 | 18,4 % |
| **Alicante** | 534.604 | 15,5 % |
| **Sevilla** | 484.431 | 12,7 % |

Además, al representar la renta de forma continua (un punto por municipio) frente a la electrificación o la antigüedad, la relación se mantiene en la misma dirección. Esto indica que el resultado no depende de los cortes elegidos para definir los quintiles.

### 4. Discusión
Los resultados respaldan con claridad H2 y H3: en los municipios de mayor renta el parque es más nuevo y está más electrificado. H1 se cumple solo parcialmente —la potencia media aumenta de forma leve y la cilindrada permanece casi constante— y H4 muestra una tendencia débil.

El EDA detectó dos bloques de variables fuertemente correlacionadas: el bloque de motor (kw, cilindrada y potencia_cv) y las seis variables de renta del INE. Para evitar redundancia, el análisis trabaja con un único representante de cada bloque (potencia_cv y renta_neta_persona).

Debe subrayarse el carácter descriptivo del estudio: los resultados expresan asociaciones observadas sobre la población completa, no relaciones de causalidad. El control del renting permite descartar que la tendencia observada sea un espejismo creado por esta modalidad. No obstante, al ser un análisis descriptivo, los resultados muestran una fuerte correlación, pero no una causalidad estricta.

### 5. Limitaciones
* **Cobertura territorial:** La DGT suprime el municipio en poblaciones de menos de 10.000 habitantes, por lo que el análisis abarca 273 municipios de ese tamaño o superior y no es extrapolable al ámbito rural.
* **Horizonte temporal:** Solo se consideran turismos matriculados desde 2010; las conclusiones se refieren a ese parque, no al histórico completo.
* **Desfase entre fuentes:** El parque es de 2026 y la renta de 2023 (último año publicado); el cruce se considera válido por la baja volatilidad de la renta municipal.
* **Naturaleza descriptiva:** El estudio describe asociaciones sobre la población completa y no establece causalidad.
* **Gama alta:** Dado que esta categoría se define mediante una lista manual de marcas y no a través de un criterio técnico oficial, esta métrica debe interpretarse como una aproximación a la realidad y no como un dato definitivo.

### 6. Conclusiones
El análisis confirma una relación clara entre la renta municipal y el perfil del parque de turismos. Los efectos más sólidos son la antigüedad y la electrificación, que descienden y aumentan, respectivamente, con la renta; la potencia muestra un efecto leve y la presencia de marcas de gama alta uno escaso. El renting introduce un sesgo apreciable pero no anula el efecto de la renta, que se confirma además entre provincias y al tratar la renta de forma continua.

Estos resultados pueden consultarse de forma interactiva en el cuadro de mando que acompaña al proyecto, donde se segmentan por provincia, año y nivel de renta.
