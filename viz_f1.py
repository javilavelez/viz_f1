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

dataset = [['driverRef', 'String', 'Identificador del piloto'], 
           ['driver_forename', 'String', 'Nombre del piloto'], 
           ['driver_surname', 'String', 'Apellido del piloto'], 
           ['driver_dob', 'Date', 'Fecha de nacimiento del piloto'], 
           ['driver_nationality', 'String', 'Nacionalidad del piloto'], 
           
           ['raceId', 'Number', 'Identificador de la carrera'], 
           ['result_number', 'Number', 'Nacionalidad del piloto'], 
           
           ['start_position', 'String', 'Nacionalidad del piloto'], 
           ['final_position', 'String', 'Nacionalidad del piloto'], 
           ['rank', 'String', 'Nacionalidad del piloto'], 
           
           ['status', 'String', 'Nacionalidad del piloto'], 
           ['circuit_reference', 'String', 'Nacionalidad del piloto'], 
           ['circuit_name', 'String', 'Nacionalidad del piloto'],
           
           ['circuit_location', 'String', 'Nacionalidad del piloto'], 
           ['circuit_country', 'String', 'Nacionalidad del piloto'], 
           ['circuit_lat', 'String', 'Nacionalidad del piloto'], 
           
           ['circuit_lng', 'String', 'Nacionalidad del piloto'], 
           ['year', 'String', 'Nacionalidad del piloto'], 
           ['race_name', 'String', 'Nacionalidad del piloto'],
           
           ['race_date', 'String', 'Nacionalidad del piloto'], 
           ['race_time', 'String', 'Nacionalidad del piloto'],
          ]

														
