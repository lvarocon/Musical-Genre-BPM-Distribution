# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:17:26 2026

@author: alvar
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Leer los datos
file_name = 'Spotify_dataset_50k_songs-inputs.csv'
df = pd.read_csv(file_name, sep = ";")

# Filtrar los 15 géneros más frecuentes
top_genres = df['genre'].value_counts().head(15).index.tolist()
df_filtered = df[df['genre'].isin(top_genres)]

# --- CAMBIO 1: Calcular promedios y ordenar géneros ---
# Agrupamos por género, calculamos la media del tempo y ordenamos de menor a mayor
genre_means = df_filtered.groupby('genre')['tempo'].mean().sort_values()

# Lista de géneros ordenados (Plotly dibuja de abajo hacia arriba)
sorted_genres = genre_means.index.tolist()

fig = go.Figure()
colors = px.colors.qualitative.Prism

# Iterar sobre los géneros ordenados por su promedio
for i, genre in enumerate(sorted_genres):
    fig.add_trace(go.Violin(
        x=df_filtered['tempo'][df_filtered['genre'] == genre],
        line_color='black',
        fillcolor=colors[i % len(colors)],
        name=genre,
        opacity=0.8,
        # Se añade una línea indicando la media para que el orden sea evidente visualmente
        meanline_visible=True 
    ))

# --- CAMBIO 2: Separar distribuciones ligeramente ---
# Se reduce el parámetro 'width' de 3 a 1.8 para disminuir el solapamiento vertical
fig.update_traces(orientation='h', side='positive', width=1.8, points=False)

fig.update_layout(
    title='Spotify Dataset : Distribución de Tempo según Género',
    xaxis_title='Tempo (BPM)',
    yaxis_title='Género',
    xaxis_showgrid=False,
    xaxis_zeroline=False,
    height=800,
    showlegend=False,
    margin=dict(l=150)
)

fig.write_html('index.html')