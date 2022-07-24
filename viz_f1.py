import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.title("Circuitos, Pilotos y Fabricantes de la (F1 1951 - 2022)")
st.markdown("***Races are won at the track. Championships are won at the factory - Mercedes (2019)***")
st.markdown('<br> La F1 es un deporte global que siguen millones de personas en todo el mundo y es fascinante ver cómo los pilotos se ponen al límite en estos vehículos para convertirse en los corredores más rápidos del mundo. </br>',unsafe_allow_html=True)

st.markdown("**Dataset**")
st.markdown('<br>El dataset contiene la información sobre las carreras de Fórmula 1, los pilotos, la clasificación, los circuitos y los campeonatos desde 1951 hasta la última temporada de 2021.</br>',unsafe_allow_html=True)

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

st.markdown("**Características del dominio**")
st.markdown('<br>El gráfico se realizará para todas las personas (hombres, mujeres y no binarios) conocedores de la F1, pero no necesariamente expertos en este tópico. Además, consideramos que el público tiene conocimeinto sobre los números (tipo) y sus aplicaciones (semántica), es decir, saben que dependiendo del contexto el número puede ser año así como también puede ser posición. (Gráfica no diseñada para niños que no saben leer o escribir, por ejemplo). </br>',unsafe_allow_html=True)

st.markdown("**Abstracción de tareas**")
st.markdown('<br> 1. Presentar la evolución de pilotos y de los fabricantes de los autos en el ranking de la F1 a través del tiempo.')
st.markdown('2. Descubrir si los mejores fabricantes de autos han cambiado en el tiempo'.)
st.markdown('3. Identificar a los mejores pilotos desde 1950 - 2022. </br>')

# Visualization
st.markdown('<br></br>',unsafe_allow_html=True)
st.markdown("**Visualizacion del dataset**")

df_f1_ranks = pd.read_csv('./drivers_f1.csv', sep=';')
df_f1_ranks['driver_name'] = df_f1_ranks['driv_name'] + ' ' + df_f1_ranks['driv_surname']
df_f1_ranks = df_f1_ranks[['driver_name', 'race_name', 'race_year', 'rank']]
df_f1_ranks['rank'] = df_f1_ranks['rank'].replace('\\N', np.nan) 
df_f1_ranks['rank'] = df_f1_ranks['rank'].replace('0', np.nan) 
df_f1_ranks = df_f1_ranks.dropna()
df_f1_ranks = df_f1_ranks.drop_duplicates()
df_f1_ranks = df_f1_ranks.astype({'driver_name': str, 'race_name': str, 'race_year': str, 'rank': int})
df_f1_ranks = df_f1_ranks.sort_values(by='rank', ascending=False)

fig = go.Figure()

driver_list = sorted(list(df_f1_ranks['driver_name'].unique()))
race_list = sorted(list(df_f1_ranks['race_name'].unique()))
year_list = sorted(list(df_f1_ranks['race_year'].unique()), reverse=True)

#color_list = px.colors.n_colors('rgb(0, 0, 0)', 'rgb(255, 255, 255)', len(driver_list), colortype='rgb')
#colors = dict(zip(driver_list, color_list))

for race, year in zip(race_list, year_list):
    fig.add_trace(
        go.Bar(
            x = df_f1_ranks['rank'][(df_f1_ranks['race_name']==race) & (df_f1_ranks['race_year']==year)],
            y = df_f1_ranks['driver_name'][(df_f1_ranks['race_name']==race) & (df_f1_ranks['race_year']==year)],
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
    height=800
)

fig.update_xaxes(title_text='Position')
fig.update_yaxes(title_text='Driver')

st.plotly_chart(fig, use_container_width=True)
