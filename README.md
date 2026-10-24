# Visualización de datos – PEC 2

Tres técnicas de visualización (bubble chart, radar chart y ridgeline chart) aplicadas a conjuntos de datos abiertos. Asignatura de Visualización de Datos, Máster en Ingeniería Informática (UOC).

## Visualizaciones

| Técnica         | Visualización                                                                                                                                                                           | Datos         |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Bubble chart    | [PIB per cápita y esperanza de vida en los diez países más poblados, 2024](https://duved.github.io/Visualizacion-de-datos-PEC2/Bubble%20chart/bubble_chart_desarrollo_mundial.html)     | Banco Mundial |
| Radar chart     | [Desarrollo humano y presión sobre el planeta, 2023](https://duved.github.io/Visualizacion-de-datos-PEC2/Radar%20Charts/radar_chart_desarrollo_humano.html)                             | PNUD          |
| Ridgeline chart | [Temperaturas máximas diarias en las grandes ciudades españolas, 2024](https://duved.github.io/Visualizacion-de-datos-PEC2/Ridgeline%20Chart/ridgeline_temperaturas_ciudades_2024.html) | NOAA NCEI     |

Cada carpeta contiene:

- `datos/`: los ficheros originales tal como se descargaron de la fuente.
- Un CSV con el subconjunto de datos usado en el gráfico.
- El script de Python que lee ese CSV y genera el HTML.
- El HTML publicado.

## Fuentes de datos

### Bubble chart – Banco Mundial

Tres indicadores de los World Development Indicators (última actualización de los ficheros: 8 de octubre de 2026), año 2024, para los diez países con más población:

| Indicador                         | Código           | Enlace                                              |
| --------------------------------- | ---------------- | --------------------------------------------------- |
| PIB per cápita (US$ corrientes)   | `NY.GDP.PCAP.CD` | https://data.worldbank.org/indicator/NY.GDP.PCAP.CD |
| Esperanza de vida al nacer (años) | `SP.DYN.LE00.IN` | https://data.worldbank.org/indicator/SP.DYN.LE00.IN |
| Población total                   | `SP.POP.TOTL`    | https://data.worldbank.org/indicator/SP.POP.TOTL    |

Ficheros originales: `Bubble chart/datos/API_*.csv` (descarga en CSV desde la página de cada indicador).

### Radar chart – PNUD

Series temporales completas de los índices compuestos del Informe sobre Desarrollo Humano 2025 (datos de 2023): esperanza de vida, años esperados y medios de escolarización, RNB per cápita (PPA 2021), emisiones de CO₂ per cápita y huella material per cápita. Los mínimos y máximos de cada eje son los de las notas técnicas del informe.

- Descarga de datos: https://hdr.undp.org/data-center/documentation-and-downloads
- Ficheros originales: `Radar Charts/datos/HDR25_Composite_indices_complete_time_series.csv` y `HDR25_Composite_indices_metadata.xlsx`.

### Ridgeline chart – NOAA NCEI (GHCN-Daily)

Temperatura máxima diaria (`TMAX`) de 2024 en una estación por ciudad, del Global Historical Climatology Network – Daily.

- Página del conjunto de datos: https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily
- Ficheros por estación: https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/
- Inventario de estaciones (`ghcnd-stations.txt`) y documentación (`readme.txt`): https://www.ncei.noaa.gov/pub/data/ghcn/daily/

| Ciudad    | Estación              |     | Código GHCN   |
| --------- | --------------------- | --- | ------------- |
| Alicante  | Alicante              |     | `SPE00101043` |
| Barcelona | Barcelona Aeropuerto  |     | `SP000008181` |
| Bilbao    | Bilbao Aeropuerto     |     | `SPE00120611` |
| Madrid    | Madrid Retiro         |     | `SP000003195` |
| Málaga    | Málaga Aeropuerto     |     | `SP000006155` |
| Murcia    | Murcia                |     | `SPE00120323` |
| Palma     | Palma de Mallorca CMT |     | `SPE00119882` |
| Sevilla   | Sevilla San Pablo     |     | `SPE00120512` |
| Valencia  | Valencia              |     | `SP000008416` |
| Zaragoza  | Zaragoza Aeropuerto   |     | `SP000009434` |

## Bibliografía

### Técnicas de visualización

- Bubble chart:
  - The Data Visualisation Catalogue. *Bubble Chart*. https://datavizcatalogue.com/methods/bubble_chart.html
  - Data Viz Project. *Bubble Chart*. https://datavizproject.com/data-type/bubble-chart/
- Radar chart:
  - The Data Visualisation Catalogue. *Radar Chart*. https://datavizcatalogue.com/methods/radar_chart.html
  - Data Viz Project. *Radar Diagram*. https://datavizproject.com/data-type/radar-diagram/
- Ridgeline chart:
  - From Data to Viz. *Ridgeline plot*. https://www.data-to-viz.com/graph/ridgeline.html
  - The R Graph Gallery. *Basic ridgeline plot*. https://r-graph-gallery.com/294-basic-ridgeline-plot.html#color

### Datos

- Banco Mundial (2026). *World Development Indicators*. Washington, D. C.: The World Bank. https://databank.worldbank.org/source/world-development-indicators [consulta: octubre de 2026].

- Menne, M. J., Durre, I., Vose, R. S., Gleason, B. E. y Houston, T. G. (2012). An overview of the Global Historical Climatology Network-Daily Database. *Journal of Atmospheric and Oceanic Technology*, 29, 897-910. https://doi.org/10.1175/JTECH-D-11-00103.1

- Menne, M. J., Durre, I., Korzeniewski, B., McNeill, S., Thomas, K., Yin, X., Anthony, S., Ray, R., Vose, R. S., Gleason, B. E. y Houston, T. G. (2012). *Global Historical Climatology Network – Daily (GHCN-Daily), Version 3*. NOAA National Climatic Data Center. https://doi.org/10.7289/V5D21VHZ [consulta: octubre de 2026].

- Programa de las Naciones Unidas para el Desarrollo (2025). *Human Development Report 2025*. Nueva York: PNUD. https://hdr.undp.org/content/human-development-report-2025 [consulta: octubre de 2026].

## Herramientas

Los gráficos se han generado con Python y [Plotly](https://plotly.com/python/). Cada script se ejecuta de forma independiente (`python bubble_chart.py`, etc.) y escribe el HTML en su misma carpeta.
