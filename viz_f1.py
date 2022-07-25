import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm

st.title("Los pilotos y fabricantes de la F1 a través del tiempo (1951 - 2021)")
st.markdown("***Races are won at the track. Championships are won at the factory - Mercedes (2019)***")
st.markdown('La F1 es un deporte global que siguen millones de personas en todo el mundo y es fascinante ver cómo los pilotos se ponen al límite en estos vehículos para convertirse en los corredores más rápidos del mundo.')

st.markdown("**Contexto**")
st.markdown('El Campeonato Mundial de Fórmula 1 es la principal competición de automovilismo internacional y el campeonato de deportes de motor más popular y prestigioso del mundo.')
st.markdown('Cada carrera de la F1 se le denomina Gran Premio y el torneo que las agrupa es el **Campeonato Mundial de Fórmula 1**.')
st.markdown('La mayoría de los circuitos de carreras donde se celebran los Grandes Premios son autódromos, aunque también se utilizan circuitos callejeros.')
st.markdown('A su vez, los automóviles utilizados son monoplazas con la última tecnología disponible, siempre limitadas por un reglamento técnico; algunas mejoras que fueron desarrolladas en la Fórmula 1 terminaron siendo utilizadas en automóviles comerciales, como el freno de disco.')
st.markdown('El inicio de la Fórmula 1 moderna se remonta al año 1950, en el que participaron escuderías como Ferrari, Alfa Romeo y Maserati, algunas reemplazadas por otras nuevas como McLaren, Williams y Red Bull.')
st.markdown('Por su parte, los pilotos deben contar con la superlicencia de la FIA para competir, que se obtiene por los resultados en otros campeonatos.')

st.markdown('*El siguiente proyecto tiene como propósito ilustrar la trayectoria de los pilotos y fabricantes de autos de la F1 a través del tiempo.*')

st.markdown("**Características del dominio**")
st.markdown('El gráfico se realizará para:')
st.markdown('1. Todas las personas (hombres, mujeres y no binarios)')
st.markdown('2. Personas conocedoras de la F1, pero no necesariamente expertas en este tópico.')
st.markdown('3. Personas con conocimeinto sobre los números (tipo) y sus aplicaciones (semántica), es decir, saben que dependiendo del contexto el número puede ser año así como también puede ser posición. (Gráfica no diseñada para niños que no saben leer o escribir, por ejemplo).')

st.markdown("**Abstracción de tareas**")
st.markdown('1. Presentar la evolución de pilotos y de los fabricantes de los autos en el ranking de la F1 a través del tiempo.')
st.markdown('2. Descubrir si los mejores fabricantes de autos han cambiado en el tiempo.')
st.markdown('3. Identificar a los mejores pilotos desde 1950 - 2021.')

st.markdown("**Abstracción de datos**")
st.markdown('El dataset contiene la información sobre las carreras de Fórmula 1, los pilotos, la clasificación, los circuitos y los campeonatos desde 1951 hasta la última temporada de 2021.')

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

# Visualization
st.markdown("**Visualizacion del dataset**")

df_f1_ranks = pd.read_csv('./drivers_f1.csv', sep=';')
df_f1_ranks['driver_name'] = df_f1_ranks['driv_name'] + ' ' + df_f1_ranks['driv_surname']
df_f1_ranks = df_f1_ranks[['driver_name', 'race_name', 'race_date', 'race_year', 'points']]
df_f1_ranks = df_f1_ranks.drop_duplicates()
df_f1_ranks = df_f1_ranks.astype({'driver_name': str, 'race_name': str, 'race_date': str, 'race_year': str, 'points': float})
df_f1_ranks["race_date"] = pd.to_datetime(df_f1_ranks["race_date"])

last_race_list = df_f1_ranks.groupby(by=["race_date"]).max().index.values
df_f1_ranks = df_f1_ranks[df_f1_ranks["race_date"].isin(last_race_list)]
df_f1_ranks = df_f1_ranks[df_f1_ranks['race_year'].astype(int)>=2004]

df_f1_ranks = df_f1_ranks.sort_values(by=['race_date', 'points'], ascending=[True, False])
df_set_index = df_f1_ranks.set_index(['race_date', 'race_year'])
df_pivoted = df_set_index.pivot_table(values='points', index=df_set_index.index, columns='driver_name', aggfunc='max', sort=False)
driver_list = sorted(list(df_f1_ranks['driver_name'].unique()))


cmap=cm.get_cmap('tab20b', len(driver_list))
color_dict = dict(zip(driver_list, cmap.colors))

db = df_pivoted
db = db.rename_axis('keys').reset_index()

db.index = range(0,len(db.index)*5,5)
row_nums = [i for i in range(0,(len(db.index)+1)) if i % 5 != 0 ]
empty = pd.DataFrame(np.nan, index= row_nums, columns = db.columns)

expand_df = pd.concat([db, empty]).sort_index()
expand_df = expand_df.interpolate()
expand_df = expand_df.fillna(method='ffill')

def update(i):
    ax.clear()
    ax.set_facecolor(plt.cm.Greys(0.2))
    
    one_row = expand_df.iloc[i][1:]
    one_row_ascending = one_row.sort_values(ascending=True)
    one_row_ascending = one_row_ascending.dropna()
    characters = one_row_ascending.index
    
    [spine.set_visible(False) for spine in ax.spines.values()]
    hbars = ax.barh(y = range(len(characters)),
           tick_label=one_row_ascending.index,
           width = one_row_ascending.values,
           height = 0.8,
           color = [color_dict[driver_name] for driver_name in characters]
           )
    ax.set_title(expand_df['keys'][i][1])
    #ax.bar_label(hbars, fmt='%.2d')
    

fig,ax = plt.subplots(#figsize=(10,7),
                      facecolor = plt.cm.Greys(0.2),
                      dpi = 150,
                      tight_layout=True
                     )

data_anime = FuncAnimation(
    fig = fig,
    func = update,
    frames= len(db),
    interval=300,
)

#st.plotly_chart(fig, use_container_width=True)
components.html(data_anime.to_jshtml(), height=600)

#HtmlFile = line_ani.to_html5_video()
#with open("myvideo.html","w") as f:
#    print(data_anime.to_html5_video(), file=f)
#    
#HtmlFile = open("myvideo.html", "r")
##HtmlFile="myvideo.html"
#source_code = HtmlFile.read() 
#components.html(source_code, height = 900,width=900)
