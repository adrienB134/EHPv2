#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

import numpy as np
import pandas as pd
import gc
import streamlit as st
import plotly.express as px
import time



gc.collect() #vide la mémoire

@st.cache()
def load_data(_uploadedFile):
    ehp_data = pd.read_csv(_uploadedFile ,sep=';', header=15)
    ehp_data = pd.DataFrame(ehp_data)
    ehp_data = (ehp_data.rename(columns={'Horodatage':'index'})
                       .set_index('index', drop = False))
    ehp_data = ehp_data.iloc[::15,:]
    return ehp_data

def RCP(ehp_data,app_mode):
    if app_mode=='900':
        container=st.container()
        Tmoy50 = st.select_slider(
            label= " date Tmoy>50°C",
            options=ehp_data.index
        )
        Tmoy51 = st.select_slider(
            label= " date Tmoy<50°C",
            options=ehp_data.index
        )
        with st.expander("Paramètres de limites"):
            TmoySup1 = st.number_input(
                label = "Tmoy supérieure à froid", 
                value = 14
            )
            TmoySup2 = st.number_input(
                label = "Tmoy supérieure à chaud",
                value = 28
            )
            TmoyInf1 = st.number_input(
                label = "Tmoy inférieure à froid",
                value = -14
            )
            TmoyInf2 = st.number_input(
                label = "Tmoy inférieure à chaud",
                value = -28
            )
        df = ehp_data[['TGRAD', 'TMOY']]  
        df2 = df.assign(Tmoymin=-14)
        df2 = df2.assign(Tmoymax=14)
        df2.loc[df2.index <= Tmoy50,'Tmoymax'] = TmoySup1
        df2.loc[df2.index > Tmoy50,'Tmoymax'] = TmoySup2
        df2.loc[df2.index > Tmoy51,'Tmoymax'] = TmoySup1
        df2.loc[df2.index <= Tmoy50,'Tmoymin'] = TmoyInf1
        df2.loc[df2.index > Tmoy50,'Tmoymin'] = TmoyInf2
        df2.loc[df2.index > Tmoy51,'Tmoymin'] = TmoyInf1

        fig_rcp = px.line(df2, title="Evolution de la pression RCP pendant l'épreuve", 
                        labels={
                        "index":"Date",
                        "value":"Pression (bar)",
                        "variable":"Valeurs"
                        })
        container.write(fig_rcp)
    else:
        st.write("Erreur")

def main():
    UploadedFile=st.sidebar.file_uploader(label="Charger le fichier de dépouillement")
    if UploadedFile != None:
        app_mode = st.sidebar.selectbox(
            'Palier',
            ['900','1300']
        )
        courbe = st.sidebar.selectbox(
            'courbe',
            [
                "Evolution de la pression RCP pendant l'épreuve",
                "Evolution de la pression de refoulement de la pompe RCV191PO",
                "Evolution de la pression de refoulement de la pompe RCV191PO - détail",
                "Température des gros composants du CPP - Fond de cuve",
                "Température des gros composants du CPP - couvercle et pressu",
                "Température des gros composants du CPP - GVs",
                "Gradients de Pression de l'EHP",
                "Suivi de la Tmoy de l'EHP",
                "Suivi du gradient de Tmoy de l'EHP",
                "Suivi des températures fluide pendant l'EHP - 1",
                "Suivi des températures fluide pendant l'EHP - 2",
                "Gradient des températures métal pendant l'EHP - Fond de cuve",
                "Gradient des températures métal pendant l'EHP - Couvercle et Pressu",
                "Gradient des températures métal pendant l'EHP - GV",
                "Evolution de la pression pendant le palier d'épreuve",
                "Evolution de la pression pendant le palier d'épreuve"
            ]
        )
        chart_data=load_data(UploadedFile)
        st.info(
            "Mettre la courbe en plein écran avant d'enregistrer en utilisant le bouton appareil photo",
            icon="⚠️"
        )

        if courbe == 'Evolution de la pression RCP pendant l\'épreuve':
           RCP(chart_data,app_mode)
        else:
            st.write("hello")


if __name__ == "__main__":
    main()
