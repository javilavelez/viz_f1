import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.title("Visualización circuitos y campeones de la F1 1951 - 2022")
st.markdown("***Races are won at the track. Championships are won at the factory - Mercedes (2019)***")
st.markdown('<br></br>',unsafe_allow_html=True)
st.markdown("La F1 es un deporte global que siguen millones de personas en todo el mundo y es fascinante ver cómo los pilotos se ponen al límite en estos vehículos para convertirse en los corredores más rápidos del mundo.")
st.markdown('<br></br>',unsafe_allow_html=True)
st.markdown("**Dataset**")
st.write("El dataset contiene la información sobre las carreras de Fórmula 1, los pilotos, la clasificación, los circuitos y los campeonatos desde 1951 hasta la última temporada de 2021.")
st.markdown('<br></br>',unsafe_allow_html=True)
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



df_f1_ranks = pd.read_csv('./drivers_f1.csv', sep=';')
df_f1_ranks['driver_name'] = df_f1_ranks['driv_name'] + ' ' + df_f1_ranks['driv_surname']
df_f1_ranks = df_f1_ranks[['driver_name', 'race_name', 'race_year', 'rank']]
df_f1_ranks['rank'] = df_f1_ranks['rank'].replace('\\N', str(df_f1_ranks['rank'].loc[df_f1_ranks['rank'].str.contains('\d')].astype(int).max()))
df_f1_ranks['rank'] = df_f1_ranks['rank'].replace('0', str(df_f1_ranks['rank'].loc[df_f1_ranks['rank'].str.contains('\d')].astype(int).max()))
df_f1_ranks = df_f1_ranks.drop_duplicates()
df_f1_ranks = df_f1_ranks.astype({'driver_name': str, 'race_name': str, 'race_year': str, 'rank': int})
df_f1_ranks = df_f1_ranks.sort_values(by='rank', ascending=False)

fig = go.Figure()

driver_list = sorted(list(df_f1_ranks['driver_name'].unique()))
race_list = sorted(list(df_f1_ranks['race_name'].unique()))
year_list = sorted(list(df_f1_ranks['race_year'].unique()), reverse=True)
year_selected = '2021'

# assign colors to type using a dictionary
colors = {'A':'steelblue',
          'B':'firebrick'}

for race, year in zip(race_list, year_list):
    fig.add_trace(
        go.Bar(
            x = df_f1_ranks['rank'][(df_f1_ranks['race_name']==race) & (df_f1_ranks['race_year']==year)],
            y = df_f1_ranks['driver_name'][(df_f1_ranks['race_name']==race) & (df_f1_ranks['race_year']==year)],
            name = race, #marker_color='lightsalmon', 
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
    height=800
)

st.plotly_chart(fig, use_container_width=True)