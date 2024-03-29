import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.graph_objects as go
from raceplotly.plots import barplot
from PIL import Image

f1 = Image.open('f1-wp.PNG')
st.image(f1)
st.title("Races are won at the track. Championships are won at the factory - Mercedes (2019)")

st.markdown('La F1 es un deporte global que siguen millones de personas en todo el mundo y es fascinante ver cómo los pilotos se ponen al límite en estos vehículos para convertirse en los corredores más rápidos del mundo.')
st.markdown('Después de explorar las visualizaciones sabrás quienes son los pilotos más rápidos del mundo, cómo fue su evolución en el deporte y también quiénes son los fabricantes (escuderías) que conforman ese *#DreamTeam*.')

# Visualization
st.title("¡Comencemos!")
driv = Image.open('drivers.PNG')
st.image(driv)

st.markdown('**¿Sabes quiénes han sido los pilotos que más campeonatos mundiales han ganado?**')
st.markdown('¡Descúbrelo en la siguiente visualización!')

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

st.markdown('**¿No te gustaría saber cómo fue su evolución en el año para llegar a ser campeón?**')
st.markdown('En esta visualización encontrarás cuántos puntos ganó cada piloto en cada uno de los Grand Pix que se corrieron durante ese año.')

df_f1_ranks = pd.read_csv('./drivers_f1.csv', sep=';')
df_f1_ranks['driver_name'] = df_f1_ranks['driv_name'] + ' ' + df_f1_ranks['driv_surname']
df_f1_ranks = df_f1_ranks[['driver_name', 'cons_name', 'cons_nationality', 'driv_nationality', 'race_name', 'race_date', 'race_year', 'points']]

df_f1_ranks = df_f1_ranks.drop_duplicates()
df_f1_ranks = df_f1_ranks.dropna()

df_f1_ranks = df_f1_ranks.astype({'driver_name': str, 'cons_name': str, 'cons_nationality': str, 'driv_nationality': str, 'race_name': str, 'race_date': str, 'race_year': str, 'points': float})
df_f1_ranks = df_f1_ranks.sort_values(by='points', ascending=True)

fig = go.Figure()

driver_list = sorted(list(df_f1_ranks['driver_name'].unique()))
race_list = sorted(list(df_f1_ranks['race_name'].unique()))
year_list = sorted(list(df_f1_ranks['race_year'].unique()), reverse=True)

#color_list = px.colors.n_colors('rgb(0, 0, 0)', 'rgb(255, 255, 255)', len(driver_list), colortype='rgb')
#colors = dict(zip(driver_list, color_list))

for race, year in zip(race_list, year_list):
    fig.add_trace(
        go.Bar(
            x = df_f1_ranks['points'][(df_f1_ranks['race_name']==race) & (df_f1_ranks['race_year']==year) & (df_f1_ranks['points']>0)],
            y = df_f1_ranks['driver_name'][(df_f1_ranks['race_name']==race) & (df_f1_ranks['race_year']==year) & (df_f1_ranks['points']>0)],
            name = race, 
            visible = True, orientation='h'
        )
    )
    
    
buttons_1 = []

for i, race in enumerate(race_list):
    args = [False] * len(race_list)
    args[i] = True
    
    button_1 = dict(label = race,
                  method = "update",
                  args=[{"visible": args}])
    
    buttons_1.append(button_1)
    
    
buttons_2 = []

for i, year in enumerate(year_list):
    args = [False] * len(year_list)
    args[i] = True
    
    button_2 = dict(label = year,
                  method = "update",
                  args=[{"visible": args}])
    
    buttons_2.append(button_2)
    
    
fig.update_layout(
    updatemenus=[dict(
                    active=0,
                    type="dropdown",
                    buttons=buttons_1,
                    x = 0,
                    y = 1.1,
                    xanchor = 'left',
                    yanchor = 'bottom'
                ), 
                dict(
                    active=0,
                    type="dropdown",
                    buttons=buttons_2,
                    x = 0.5,
                    y = 1.1,
                    xanchor = 'left',
                    yanchor = 'bottom'
                )
                ], 
    autosize=False,
    width=1000,
    height=800,
)

fig.update_xaxes(title_text='Points')
fig.update_yaxes(title_text='Driver')

st.plotly_chart(fig, use_container_width=True)

st.markdown('**Bueno, y qué sería de un piloto sin su escudería...**')
st.markdown('Aquí podrás conocer los fabricantes de los autos más rápidos de la F1')

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

st.markdown("**Realizado por Estudiantes MIA: Juliana Ávila y Aquiles Martinez**")
