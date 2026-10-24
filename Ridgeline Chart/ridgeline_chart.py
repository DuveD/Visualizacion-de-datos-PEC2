"""Ridgeline chart: temperaturas máximas diarias de 2024 en diez ciudades españolas.

Lee ridgeline_temperaturas_ciudades_2024.csv y genera ridgeline_temperaturas_ciudades_2024.html.
"""
import csv
import statistics
from pathlib import Path

import plotly.graph_objects as go

CARPETA = Path(__file__).resolve().parent
ALTURA = 1.3  # altura de cada cresta, en filas (>1: se solapa con la de arriba)
# Degradado de 15 °C (azul, frío) a 40 °C (amarillo, calor), con fucsia en 25 °C
GRADIENTE = [[0, 'rgb(30, 80, 220)'], [0.4, 'rgb(230, 0, 170)'], [1, 'rgb(255, 210, 0)']]

# Leer las temperaturas de cada ciudad
temps = {}
with open(CARPETA / 'ridgeline_temperaturas_ciudades_2024.csv', newline='', encoding='utf-8') as f:
    for fila in csv.DictReader(f):
        temps.setdefault(fila['Ciudad'], []).append(float(fila['Temperatura máxima (°C)']))

# Ciudades de menor a mayor mediana; la primera va arriba del todo
ciudades = sorted(temps, key=lambda c: statistics.median(temps[c]))
altura_fila = {c: len(ciudades) - 1 - i for i, c in enumerate(ciudades)}

fig = go.Figure()

# Una cresta por ciudad. Se dibujan de arriba abajo para que cada una tape la base de la anterior.
for ciudad in ciudades:
    v = temps[ciudad]
    # Curva de densidad: KDE gaussiano con el ancho de banda de Silverman,
    # calculado solo entre la mínima y la máxima de la ciudad
    q1, _, q3 = statistics.quantiles(v, n=4)
    densidad = statistics.kde(v, h=0.9 * min(statistics.stdev(v), (q3 - q1) / 1.34) * len(v) ** -0.2)
    xs = [min(v) + (max(v) - min(v)) * k / 199 for k in range(200)]
    ys = [densidad(x) for x in xs]
    base = altura_fila[ciudad]
    fig.add_trace(go.Scatter(
        x=xs + xs[::-1],
        y=[base + ALTURA * y / max(ys) for y in ys] + [base] * len(xs),
        fill='toself',
        fillgradient=dict(type='horizontal', colorscale=GRADIENTE, start=15, stop=40),
        line=dict(color='black', width=1.5),
        hoverinfo='skip',
    ))

# Raya negra en la mediana de cada ciudad
fig.add_trace(go.Scatter(
    x=[statistics.median(temps[c]) for c in ciudades],
    y=[altura_fila[c] for c in ciudades],
    text=ciudades,
    mode='markers',
    marker=dict(symbol='line-ns', size=12, color='black', line=dict(color='black', width=2)),
    hovertemplate='%{text}: mediana %{x:.1f} °C<extra></extra>',
))

fig.add_annotation(x=42.9, y=altura_fila['Bilbao'], ax=-10, ay=-38, text='11 ago: 42,9 °C', arrowhead=0)
fig.add_annotation(text='Fuente: NOAA NCEI, GHCN-Daily. Una estación por ciudad; 3.636 días con dato.',
                   xref='paper', yref='paper', x=0, y=-0.12, xanchor='left', showarrow=False)

fig.update_layout(
    template='simple_white',
    title=dict(text='Temperaturas máximas diarias en las grandes ciudades españolas, 2024',
               subtitle=dict(text='Cada curva muestra cómo se reparten los días del año según su temperatura máxima.'
                                  ' La raya negra es la mediana.')),
    xaxis=dict(title='Temperatura máxima diaria (°C)', range=[0, 45], dtick=5, ticksuffix=' °C', showgrid=True),
    yaxis=dict(tickvals=list(altura_fila.values()), ticktext=list(altura_fila), showline=False, ticks=''),
    separators=',.',  # coma decimal
    showlegend=False,
    height=800,
)

fig.write_html(CARPETA / 'ridgeline_temperaturas_ciudades_2024.html', include_plotlyjs='cdn')
