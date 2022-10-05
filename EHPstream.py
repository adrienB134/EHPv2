import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import pandas as pd
import gc
import streamlit as st
import plotly.express as px



gc.collect() #vide la mémoire

@st.cache
def load_data(_uploadedFile):
    EHPdata = pd.read_csv(_uploadedFile ,sep=';', header=15)


    #print(EHPdata)

    #Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True)

    #chart_data = pd.concat([Date,EHPdata.EHP001MP], axis=0)
    chart_data = pd.DataFrame(EHPdata)
    chart_data = chart_data.rename(columns={'Horodatage':'index'}).set_index('index', drop = False)

    chart_data2 = chart_data.iloc[::30,:]

    return chart_data2


app_mode = st.sidebar.selectbox('Select Page',['900','1300'])
uploaded_file = st.sidebar.file_uploader(label="Charger le fichier de dépouillement")
chart_data=load_data(uploaded_file)
Tmoy50 = st.sidebar.select_slider(label= " date Tmoy>50°C",options=chart_data.index)
Tmoy51 = st.sidebar.select_slider(label= " date Tmoy<50°C",options=chart_data.index)

tab1, tab2 = st.tabs(["1", "2"])

with tab1:
   #st.dataframe(chart_data2.iloc[:,0:2])
   #st.line_chart(chart_data2.iloc[:,0:2], height=800, use_container_width=True)
 

   df = chart_data[['TGRAD', 'TMOY']]
   
   df2 = df.assign(Tmoymin=-14)
   df2 = df2.assign(Tmoymax=14)
   df2.loc[df2.index<Tmoy50,'Tmoymax'] = 14
   df2.loc[df2.index>Tmoy50,'Tmoymax'] = 28
   df2.loc[df2.index>Tmoy51,'Tmoymax'] = 14
   
   df2.loc[df2.index>Tmoy50,'Tmoymin'] = -28
   df2.loc[df2.index>Tmoy51,'Tmoymin'] = -14
   st.write(df2)
   fig2 = px.line(df2) 
   st.write(fig2)

with tab2:
    st.write("hello")
    #fig1,ax1 = plt.subplots()
    #plt.plot(Date,EHPdata.EHP001MP, label='EHP001MP')
    #plt.plot(Date,EHPdata.EHP002MP, label='EHP002MP')
    #plt.title("Evolution de la pression RCP pendant l'épreuve")
    #plt.xlabel("Date")
    #plt.ylabel("Pression (bar)")
    #plt.xticks(rotation=30)
    #ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    #st.write(fig1)

