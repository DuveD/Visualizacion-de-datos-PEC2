"""Bubble chart: PIB per cápita frente a esperanza de vida en los diez países más poblados, 2024.

Lee bubble_chart_desarrollo_mundial.csv y genera bubble_chart_desarrollo_mundial.html.
"""
import csv
import math
from pathlib import Path

import plotly.graph_objects as go

CARPETA = Path(__file__).resolve().parent
DIAMETRO_MAX = 60  # diámetro en píxeles de la burbuja más grande
# Etiquetas que se solapan si van en el centro de la burbuja (el resto va centrado)
POSICION_ETIQUETA = {'Ethiopia': 'bottom center', 'Pakistan': 'top center'}
# Azul de claro (menos población) a oscuro (más población)
AZULES = [[0, '#86b6ef'], [0.5, '#2a78d6'], [1, '#0d366b']]

# Leer los datos
with open(CARPETA / 'bubble_chart_desarrollo_mundial.csv', newline='', encoding='utf-8') as f:
    filas = list(csv.DictReader(f))

paises = [fila['Country'] for fila in filas]
pib = [float(fila['GDP_per_capita_USD']) for fila in filas]
esperanza = [float(fila['Life_expectancy_years']) for fila in filas]
poblacion = [int(fila['Population']) for fila in filas]

fig = go.Figure(go.Scatter(
    x=pib,
    y=esperanza,
    text=paises,
    customdata=poblacion,
    mode='markers+text',
    textposition=[POSICION_ETIQUETA.get(p, 'middle center') for p in paises],
    textfont=dict(color=['white' if p > 1e9 else '#0b0b0b' for p in poblacion]),  # blanco sobre las más oscuras
    # El área de cada burbuja es proporcional a la población.
    # El color también sigue la población, en escala logarítmica: con una lineal, ocho de los diez
    # países (entre 132 y 340 millones) saldrían casi del mismo tono.
    marker=dict(size=poblacion, sizemode='area', sizeref=2 * max(poblacion) / DIAMETRO_MAX ** 2,
                color=[math.log10(p) for p in poblacion], colorscale=AZULES, showscale=True,
                colorbar=dict(title='Población', tickvals=[math.log10(m * 1e6) for m in (150, 300, 600, 1200)],
                              ticktext=['150 M', '300 M', '600 M', '1.200 M']),
                opacity=0.85, line=dict(color='white', width=1.5)),
    hovertemplate='<b>%{text}</b><br>PIB per cápita: %{x:,.0f} USD<br>'
                  'Esperanza de vida: %{y:.1f} años<br>Población: %{customdata:,} hab.<extra></extra>',
))

fig.add_annotation(text='Fuente: Banco Mundial, World Development Indicators.',
                   xref='paper', yref='paper', x=0, y=-0.15, xanchor='left', showarrow=False)

fig.update_layout(
    template='simple_white',
    title=dict(text='PIB per cápita y esperanza de vida en los diez países más poblados, 2024',
               subtitle=dict(text='El área de cada burbuja es proporcional a la población; '
                                  'el color, de claro a oscuro, también indica la población.')),
    # Escala logarítmica: el PIB per cápita va de unos 1.000 a 86.000 USD
    xaxis=dict(title='PIB per cápita (USD corrientes, escala logarítmica)', type='log',
               tickvals=[1000, 2000, 5000, 10000, 20000, 50000, 100000], tickformat=',', showgrid=True),
    yaxis=dict(title='Esperanza de vida al nacer (años)', showgrid=True),
    separators=',.',  # coma decimal
    showlegend=False,
    height=650,
)

fig.write_html(CARPETA / 'bubble_chart_desarrollo_mundial.html', include_plotlyjs='cdn')
