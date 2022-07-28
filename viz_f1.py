import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from raceplotly.plots import barplot

st.title("Los pilotos y fabricantes de la F1 a través del tiempo)")
st.markdown("***Races are won at the track. Championships are won at the factory - Mercedes (2019)***")
st.markdown('La F1 es un deporte global que siguen millones de personas en todo el mundo y es fascinante ver cómo los pilotos se ponen al límite en estos vehículos para convertirse en los corredores más rápidos del mundo.')
st.markdown('El dataset contiene la información sobre las carreras de Fórmula 1, los pilotos, la clasificación, los circuitos y los campeonatos desde 1951 hasta la última temporada de 2021.')

# Visualization
st.markdown("**Visualizacion del dataset**")

st.markdown("***Puntos ganados por pilotos en cada carrera 2004-2021***")

df_f1_ranks = pd.read_csv('./drivers_f1.csv', sep=';')
df_f1_ranks['driver_name'] = df_f1_ranks['driv_name'] + ' ' + df_f1_ranks['driv_surname']
df_f1_ranks = df_f1_ranks[['driver_name', 'cons_name', 'cons_nationality', 'driv_nationality', 'race_name', 'race_date', 'race_year', 'points']]

df_f1_ranks = df_f1_ranks.drop_duplicates()

df_f1_ranks = df_f1_ranks.astype({'driver_name': str, 'cons_name': str, 'cons_nationality': str, 'driv_nationality': str, 'race_name': str, 'race_date': str, 'race_year': str, 'points': float})
df_f1_ranks["race_date"] = pd.to_datetime(df_f1_ranks["race_date"], format='%d-%m-%Y')
df_f1_ranks = df_f1_ranks[df_f1_ranks['race_year'].astype(int)>=2004]
df_f1_ranks["race_year"] = pd.to_datetime(df_f1_ranks["race_year"], format='%Y')

df_f1_ranks = df_f1_ranks.sort_values(by=['race_date', 'points'], ascending=[True, False])

df_f1_ranks_agg_pilotos = df_f1_ranks.groupby(by=['driver_name', 'race_name', 'race_date', 'race_year'], sort=False, as_index=False).sum()

raceplot_1 = barplot(df_f1_ranks_agg_pilotos,  item_column='driver_name',  extra_item='race_name', value_column='points', time_column='race_date', top_entries=10)
fig_1=raceplot_1.plot(item_label = 'Piloto', 
                  value_label = 'Puntos', 
                  time_label = 'Carrera: ',
                  frame_duration = 300, 
                  date_format='%Y-%m-%d', 
                  orientation='horizontal'
)
fig_1.update_layout(
                title='Top 10 - Pilotos de F1',
                autosize=False,
                width=1000,
                height=800,
                paper_bgcolor="lightgray",
)
fig_1.update_layout(
    font_family="Courier New",
    font_color="black",
    title_font_family="Times New Roman",
    title_font_color="black",
    legend_title_font_color="black"
)
st.plotly_chart(fig_1, use_container_width=True)


st.markdown("***Campeonatos ganados por pilotos 1951-2021***")


df_f1_ranks = pd.read_csv('./drivers_f1.csv', sep=';')
df_f1_ranks['driver_name'] = df_f1_ranks['driv_name'] + ' ' + df_f1_ranks['driv_surname']
df_f1_ranks = df_f1_ranks[['driver_name', 'cons_name', 'cons_nationality', 'driv_nationality', 'race_name', 'race_date', 'race_year', 'points']]

df_f1_ranks = df_f1_ranks.drop_duplicates()

df_f1_ranks = df_f1_ranks.astype({'driver_name': str, 'cons_name': str, 'cons_nationality': str, 'driv_nationality': str, 'race_name': str, 'race_date': str, 'race_year': str, 'points': float})
df_f1_ranks["race_date"] = pd.to_datetime(df_f1_ranks["race_date"], format='%d-%m-%Y')
#df_f1_ranks = df_f1_ranks[df_f1_ranks['race_year'].astype(int)>=2004]
df_f1_ranks["race_year"] = pd.to_datetime(df_f1_ranks["race_year"], format='%Y')

last_race_date_list = df_f1_ranks.groupby(by=["race_year"]).max().race_date.values
df_f1_ranks = df_f1_ranks[df_f1_ranks["race_date"].isin(last_race_date_list)]
df_last_race_date = pd.DataFrame(last_race_date_list, columns=['full_date'])
df_f1_ranks_ganadores = df_f1_ranks[df_f1_ranks.groupby(by=['race_year']).points.transform('max') == df_f1_ranks['points']].copy()
df_last_race_date['key'] = 1
df_f1_ranks_ganadores['key'] = 1
df_f1_ranks_ganadores_cum = df_f1_ranks_ganadores.merge(df_last_race_date, on='key', how='outer').drop("key", 1)
df_f1_ranks_ganadores_cum = df_f1_ranks_ganadores_cum[df_f1_ranks_ganadores_cum.race_date <= df_f1_ranks_ganadores_cum.full_date]

df_f1_ranks_agg_pilotos_campeones = df_f1_ranks_ganadores_cum.groupby(by=['driver_name', 'full_date'], sort=False, as_index=False).count().sort_values(by=['full_date', 'points'], ascending=[True, False]).reset_index(drop=True)[['driver_name', 'full_date', 'points']]

df_f1_ranks_agg_pais_pilotos_campeones = df_f1_ranks_ganadores_cum.groupby(by=['driv_nationality', 'full_date'], sort=False, as_index=False).count().sort_values(by=['full_date', 'points'], ascending=[True, False]).reset_index(drop=True)[['driv_nationality', 'full_date', 'points']]

df_f1_ranks_agg_escuederia_campeones = df_f1_ranks_ganadores_cum.groupby(by=['cons_name', 'full_date'], sort=False, as_index=False).count().sort_values(by=['full_date', 'points'], ascending=[True, False]).reset_index(drop=True)[['cons_name', 'full_date', 'points']]

df_f1_ranks_agg_pais_escuederia_campeones = df_f1_ranks_ganadores_cum.groupby(by=['cons_nationality', 'full_date'], sort=False, as_index=False).count().sort_values(by=['full_date', 'points'], ascending=[True, False]).reset_index(drop=True)[['cons_nationality', 'full_date', 'points']]


raceplot_2 = barplot(df_f1_ranks_agg_pilotos_campeones,  item_column='driver_name',  value_column='points', time_column='full_date', top_entries=10)
fig_2=raceplot_2.plot(item_label = 'Pilotos', 
                  value_label = 'Campeonatos', 
                  time_label = 'Año: ',
                  frame_duration = 500, 
                  date_format='%Y', 
                  orientation='horizontal'
)
fig_2.update_layout(
                title='Top 10 - Pilotos de F1',
                autosize=False,
                width=1000,
                height=800,
                paper_bgcolor="lightgray",
)
fig_2.update_layout(
    font_family="Courier New",
    font_color="black",
    title_font_family="Times New Roman",
    title_font_color="black",
    legend_title_font_color="black"
)
st.plotly_chart(fig_2, use_container_width=True)


st.markdown("***Campeonatos ganados por naciones de pilotos 1951-2021***")

raceplot_5 = barplot(df_f1_ranks_agg_pais_pilotos_campeones,  item_column='driv_nationality',  value_column='points', time_column='full_date', top_entries=5)
fig_5=raceplot_5.plot(item_label = 'Paises', 
                  value_label = 'Campeonatos', 
                  time_label = 'Año: ',
                  frame_duration = 500, 
                  date_format='%Y', 
                  orientation='horizontal'
)
fig_5.update_layout(
                title='Top 5 - Nacionalidad de Pilotos de F1',
                autosize=False,
                width=1000,
                height=800,
                paper_bgcolor="lightgray",
)
fig_5.update_layout(
    font_family="Courier New",
    font_color="black",
    title_font_family="Times New Roman",
    title_font_color="black",
    legend_title_font_color="black"
)
st.plotly_chart(fig_5, use_container_width=True)


st.markdown("***Capeonatos ganados por escuderias 1951-2021***")

raceplot_3 = barplot(df_f1_ranks_agg_escuederia_campeones,  item_column='cons_name',  value_column='points', time_column='full_date', top_entries=5)
fig_3=raceplot_3.plot(item_label = 'Escuderias', 
                  value_label = 'Campeonatos', 
                  time_label = 'Año: ',
                  frame_duration = 500, 
                  date_format='%Y', 
                  orientation='horizontal'
)
fig_3.update_layout(
                title='Top 5 - Escuderias de F1',
                autosize=False,
                width=1000,
                height=800,
                paper_bgcolor="lightgray",
)
fig_3.update_layout(
    font_family="Courier New",
    font_color="black",
    title_font_family="Times New Roman",
    title_font_color="black",
    legend_title_font_color="black"
)
st.plotly_chart(fig_3, use_container_width=True)


st.markdown("***Campeonatos ganados por naciones de escuderias 1951-2021***")

raceplot_4 = barplot(df_f1_ranks_agg_pais_escuederia_campeones,  item_column='cons_nationality',  value_column='points', time_column='full_date', top_entries=5)
fig_4=raceplot_4.plot(item_label = 'Paises', 
                  value_label = 'Campeonatos', 
                  time_label = 'Año: ',
                  frame_duration = 500, 
                  date_format='%Y', 
                  orientation='horizontal'
)
fig_4.update_layout(
                title='Top 5 - Nacionalidad de Escuderias de F1',
                autosize=False,
                width=1000,
                height=800,
                paper_bgcolor="lightgray",
)
fig_4.update_layout(
    font_family="Courier New",
    font_color="black",
    title_font_family="Times New Roman",
    title_font_color="black",
    legend_title_font_color="black"
)
st.plotly_chart(fig_4, use_container_width=True)

st.markdown('*El proyecto tuvo como propósito ilustrar la trayectoria de los pilotos y fabricantes de autos de la F1 a través del tiempo.*')

st.markdown("**Características del dominio**")
st.markdown('El gráfico fue realizado para:')
st.markdown('1. Todas las personas (hombres, mujeres y no binarios)')
st.markdown('2. Personas conocedoras del deporte, específicamente de cómo se determinan los points por cada Grand Pix del año. (Gráfica realizada para personas que conocen que se reinician los puntos de forma anual y la forma en la que se asignan los puntos por carrera.)')
st.markdown('3. Personas con conocimiento sobre los números (tipo) y sus aplicaciones (semántica), es decir, saben que dependiendo del contexto el número puede ser año así como también puede significar cantidad de puntos ganados en la carrera. (Gráfica no diseñada para niños que no saben leer o escribir, por ejemplo).')

st.markdown("**Abstracción de tareas**")
st.markdown('1. Presentar la evolución de pilotos en la obtención de puntos por año y su trayectoria 2004-2021')
st.markdown('2. Ilustrar la cantidad de Campeonatos Mundiales ganados por piloto, fabricante y nacionalidad de la escudería y del piloto para el peridoo 1950-2021')
st.markdown('3. Descubrir si los mejores fabricantes de autos han cambiado en el tiempo.')
st.markdown('4. Identificar al top 10 de pilotos desde 1950 - 2021.')
st.markdown('5. Conocer de qué país son los autos y pilotos con más Campeonatos Mundiales ganados.')

st.markdown("**Abstracción de datos**")
st.markdown('El dataset contiene la información sobre las carreras de Fórmula 1, los pilotos, la clasificación, los circuitos y los campeonatos desde 2004 hasta la última temporada de 2021.')

st.markdown("**Descripción del dataset**")

dataset = [
	['raceId','Number','ID de la carrera'],
	['race_year','Number','Año de la carrera'],
	['round','Number','Round del año'],
	['race_name','String','Nombre de la carrera'],
	['race_date','Date','Fecha de la carrera'],
	['driverId','Number','ID del piloto'],
	['driv_name','String','Nombre del piloto'],
	['driv_surname','String','Apellido del piloto'],
	['driv_dob','Date','Fecha de nacimiento del piloto'],
	['driv_nationality','String','Nacionalidad del piloto'],
	['constructorId','Number','ID del fabricante'],
	['cons_name','String','Nombre del fabricante'],
	['cons_nationality','String','Nacionalidad del fabricante'],
	['start_position','Number','Posición inicial del piloto en la carrera'],
	['final_position','Number','Posición final del piloto en la carrera'],
	['rank','Number','Ranking del piloto']
        ]

df_data = pd.DataFrame(dataset, columns=['Variable','Tipo','Descripción'])
st.table(df_data)

