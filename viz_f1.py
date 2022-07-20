import streamlit as st
import pandas as pd
import numpy as np

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

														
