"""Radar chart: desarrollo humano y presión sobre el planeta, 2023.

Lee radar_chart_europa.csv y radar_chart_poblados.csv y genera radar_chart_desarrollo_humano.html.
"""
import csv
import math
from pathlib import Path

import plotly.graph_objects as go

CARPETA = Path(__file__).resolve().parent
GRUPOS = {'Vecinos europeos': 'radar_chart_europa.csv', 'Países más poblados': 'radar_chart_poblados.csv'}

# Ejes en orden: columna del CSV -> (etiqueta del eje, mínimo, máximo).
# Mínimos y máximos del PNUD (HDR 2025, notas técnicas 1 y 6). La renta usa logaritmos.
# CO₂ y huella material van invertidos: más hacia fuera = menos presión por habitante.
EJES = {
    'Esperanza de vida (años)': ('Esperanza de vida', 20, 85),
    'Escolarización esperada (años)': ('Escolarización esperada', 0, 18),
    'Escolarización media (años)': ('Escolarización media', 0, 15),
    'RNB per cápita (PPA 2021 $)': ('Renta per cápita', 100, 75000),
    'CO₂ per cápita (t)': ('Menos CO₂ per cápita', 0, 76.61),
    'Huella material per cápita (t)': ('Menos huella material', 0, 90.27),
}
INVERTIDOS = ('CO₂ per cápita (t)', 'Huella material per cápita (t)')

# España siempre azul y es la única con relleno; el resto por orden de fila, cada uno con su símbolo.
COLORES = ['#2a78d6', '#e34948', '#1baf7a', '#eda100', '#008300']
SIMBOLOS = ['circle', 'square', 'diamond', 'triangle-up', 'x']


def indice(columna, valor):
    """Pasa un valor original a la escala 0-100 del eje."""
    _, minimo, maximo = EJES[columna]
    if columna.startswith('RNB'):
        valor, minimo, maximo = math.log(valor), math.log(minimo), math.log(maximo)
    escala = (maximo - valor if columna in INVERTIDOS else valor - minimo) / (maximo - minimo)
    return 100 * max(0, min(1, escala))


def numero(valor):
    """Formato español: 46.008 o 83,7."""
    return f'{valor:,.0f}'.replace(',', '.') if valor >= 1000 else f'{valor:.1f}'.replace('.', ',')


fig = go.Figure()
grupo_de_cada_traza = []

for grupo, fichero in GRUPOS.items():
    with open(CARPETA / fichero, newline='', encoding='utf-8') as f:
        filas = list(csv.DictReader(f))
    for i, fila in enumerate(filas):
        etiquetas = [eje[0] for eje in EJES.values()]
        r = [indice(col, float(fila[col])) for col in EJES]
        # Texto del tooltip con el valor original: "Esperanza de vida: 83,7 años"
        textos = [f'{col.split(" (")[0]}: {numero(float(fila[col]))} {col.split(" (")[1][:-1]}' for col in EJES]
        mundo = fila['Tipo'] == 'Agregado'
        color = '#898781' if mundo else COLORES[i]
        fig.add_trace(go.Scatterpolar(
            r=r + r[:1], theta=etiquetas + etiquetas[:1], customdata=textos + textos[:1],  # cerrar el polígono
            name=fila['Entidad'],
            visible=grupo == 'Vecinos europeos',
            mode='lines+markers',
            line=dict(color=color, width=2, dash='dash' if mundo else 'solid'),
            marker=dict(size=8, symbol='circle' if mundo else SIMBOLOS[i]),
            fill='toself' if fila['Entidad'] == 'España' else 'none',
            fillcolor='rgba(42, 120, 214, 0.15)',
            hovertemplate='<b>%{fullData.name}</b><br>%{customdata}<br>Índice: %{r:.0f} de 100<extra></extra>',
        ))
        grupo_de_cada_traza.append(grupo)

# Botones para cambiar de grupo de países
botones = [dict(label=g, method='update', args=[{'visible': [x == g for x in grupo_de_cada_traza]}])
           for g in GRUPOS]

fig.add_annotation(text='Fuente: PNUD, Informe sobre Desarrollo Humano 2025 (datos de 2023).<br>'
                        'El área del polígono no es un índice.',
                   xref='paper', yref='paper', x=0, y=-0.12, xanchor='left', align='left', showarrow=False)

fig.update_layout(
    template='simple_white',
    title=dict(text='Desarrollo humano y presión sobre el planeta, 2023',
               subtitle=dict(text='Cada eje va de 0 a 100 con los mínimos y máximos del PNUD: más hacia fuera es mejor.<br>'
                                  'En CO₂ y huella material, más hacia fuera = menos presión por habitante.')),
    updatemenus=[dict(type='buttons', direction='right', buttons=botones, x=0, y=1.04, xanchor='left')],
    polar=dict(
        radialaxis=dict(range=[0, 100], tickvals=[20, 40, 60, 80, 100], angle=60, showline=False,
                        gridcolor='#e1e0d9', tickfont=dict(color='#898781')),
        angularaxis=dict(rotation=90, direction='clockwise', gridcolor='#e1e0d9'),
    ),
    separators=',.',  # coma decimal
    margin=dict(t=190, l=130, r=130, b=100),
    height=750,
)

fig.write_html(CARPETA / 'radar_chart_desarrollo_humano.html', include_plotlyjs='cdn')
