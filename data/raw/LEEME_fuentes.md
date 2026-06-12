# Fuentes de datos (data/raw)

Los ficheros de microdatos de la DGT son demasiado grandes para versionarse en GitHub
(ver .gitignore). Para reproducir el proyecto, descarga las fuentes desde su origen y
colócalas en esta carpeta:

- **parque_vehiculos_202603.txt** — Microdatos del parque de vehículos.
  DGT · https://www.dgt.es/  (sección "DGT en cifras" → microdatos del parque)
  https://www.dgt.es/microdatos/Parque/parque_vehiculos_202603_PROVINCIA.zip

- **30824.csv** — Atlas de Distribución de Renta de los Hogares (municipal).
  INE · INEbase → Atlas de Distribución de Renta de los Hogares
  https://www.ine.es/uc/qJx5u9nP

- **codprov.xls** — Relación de provincias y sus códigos.
  INE · https://www.ine.es/daco/daco42/clasificaciones/codprov.xls

## Documentación oficial de la fuente

- **Interfaz-de-Salida-Fichero-Parque-Anual.pdf** — Diccionario oficial de la DGT:
  descripción de los campos y códigos del fichero del parque (PROPULSION, CATELECT,
  ALIMENTACION, PROCEDENCIA, RENTING, etc.) y las reglas de anonimización de la fuente.
  Se incluye en esta misma carpeta como referencia del proyecto.

## Copia de conveniencia de las fuentes

El fichero de microdatos de la DGT es grande y los portales oficiales pueden cambiar con
el tiempo. Para facilitar la reproducción se ofrece una copia comprimida de las tres
fuentes en Google Drive:

  https://drive.google.com/file/d/1kafObKuMATrOnIRtjg40ZXKOobKG5pAq/view?usp=drive_link

Las URLs oficiales indicadas arriba son la fuente autorizada; el enlace de Drive es solo
una copia de conveniencia y no sustituye a aquellas.
