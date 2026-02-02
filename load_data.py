import pandas as pd
import streamlit as st


@st.cache_data
def load_df():
    """
    Carga el dataset principal de la app.
    """
    df = pd.read_csv("C:\\FFCV APP\\data\\df.csv")

    return df


def get_team_logos():
    """
    Diccionario Equipo → path del logo
    """
    return {
        "Benferri Cf": "logos/Benferri Cf.png",
        "Betis Florida": "logos/Betis Florida.png",
        "Cd El Campello": "logos/Cd El Campello.png",
        "Cd Montesinos": "logos/Cd Montesinos.png",
        "Catral Castrum Cf": "logos/Catral Castrum Cf.png",
        "Muro Cf": "logos/Muro Cf.png",
        "Santa Pola Cf": "logos/Santa Pola Cf.png",
        "Teulada Moraira": "logos/Teulada Moraira.png",
        "Atletico Algorfa": "logos/Atletico Algorfa.png",
        "Villena Cf": "logos/Villena Cf.png",
        "Cd Almoradi": "logos/Cd Almoradi.png",
        "Novelda Cf": "logos/Novelda Cf.png",
        "Cd Murada": "logos/Cd Murada.png",
        "Atletico Jonense": "logos/Atletico Jonense.png",
        "Callosa Deportiva": "logos/Callosa Deportiva.png",
        "Cd Contestano": "logos/Cd Contestano.png",
    }
