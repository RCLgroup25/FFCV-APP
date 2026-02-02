import streamlit as st
import pandas as pd
import os
from utils.load_data import load_df, get_team_logos
from utils.ui import team_selector

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="RCL Scout Group - Scouting 2026", layout="wide")

# --- 2. FUNCIONES DE CARGA (LOAD DATA) ---
@st.cache_data
def load_df():
    """
    Carga el dataset. 
    IMPORTANTE: El archivo debe estar en la carpeta 'data' en tu GitHub.
    """
    # Cambiamos la ruta de C:\\... a una ruta que entienda la nube
    # Si el archivo está en la raíz de tu GitHub, deja solo "df.csv"
    # Si está dentro de una carpeta llamada data, usa "data/df.csv"
    ruta_nube = "data/df.csv" 
    
    if os.path.exists(ruta_nube):
        return pd.read_csv(ruta_nube)
    else:
        # Por si lo subiste suelto a GitHub
        return pd.read_csv("df.csv")

def get_team_logos():
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

# --- 3. FUNCIONES DE INTERFAZ (UI) ---
def team_selector(team_logos, cols=6):
    if "equipo_seleccionado" not in st.session_state:
        st.session_state.equipo_seleccionado = None

    st.markdown("### 🏟️ Selecciona un equipo")

    teams = list(team_logos.keys())
    rows = [teams[i:i + cols] for i in range(0, len(teams), cols)]

    for row in rows:
        columns = st.columns(cols)
        for col, team in zip(columns, row):
            with col:
                # Intentar cargar imagen, si no existe no rompe la app
                try:
                    st.image(team_logos[team], use_container_width=True)
                except:
                    st.warning(f"Sin logo: {team}")

                if st.button(team, key=f"btn_{team}", use_container_width=True):
                    st.session_state.equipo_seleccionado = team

    return st.session_state.equipo_seleccionado

# --- 4. LÓGICA PRINCIPAL (LO QUE ANTES ERA APP.PY) ---
st.title("⚽ RCL Scout Group: Inteligencia Grupo 4")

# Cargar datos
try:
    df = load_df()
    logos = get_team_logos()

    # Selector
    equipo = team_selector(logos)

    if equipo:
        st.divider()
        st.header(f"Análisis de {equipo}")
        
        # Filtrar datos por equipo
        df_equipo = df[df['Equipo'] == equipo] if 'Equipo' in df.columns else df
        st.dataframe(df_equipo)
        
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Asegúrate de que el archivo 'df.csv' esté en la carpeta 'data' de tu GitHub.")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="FFCV | Análisis de Jugadores",
    layout="wide"
)

st.title("⚽ FFCV – Análisis por Equipo y Jugador")
st.caption(
    "Herramienta descriptiva para scouting y cuerpos técnicos. "
    "Las métricas reflejan uso, impacto y comportamiento competitivo."
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = load_df()
team_logos = get_team_logos()

# --------------------------------------------------
# FILTRO GLOBAL: MINUTOS
# --------------------------------------------------
st.markdown("### ⏱️ Filtro global")
min_minutos = st.slider(
    "Minutos mínimos jugados",
    min_value=0,
    max_value=int(df["Minutos"].max()),
    value=300,
    step=50
)

df = df[df["Minutos"] >= min_minutos]

# --------------------------------------------------
# SELECTOR DE EQUIPO
# --------------------------------------------------
equipo = team_selector(team_logos)

if not equipo:
    st.stop()

st.markdown(f"## 🏟️ {equipo}")

df_team = df[df["Equipo"] == equipo]

if df_team.empty:
    st.warning("No hay jugadores con ese filtro de minutos.")
    st.stop()

# --------------------------------------------------
# TABLA GENERAL DEL EQUIPO
# --------------------------------------------------
st.markdown("### 📋 Plantel del equipo")

st.dataframe(
    df_team[
        [
            "Jugador",
            "Posicion_Limpia",
            "Minutos",
            "Partidos_Jugados",
            "Pct_Titularidad_Real",
            "Goles",
            "Goles_p90",
            "Tarjetas_Totales"
        ]
    ].sort_values("Minutos", ascending=False),
    use_container_width=True
)

# --------------------------------------------------
# SELECTOR DE JUGADOR
# --------------------------------------------------
st.markdown("### 👤 Análisis individual")

jugador = st.selectbox(
    "Selecciona jugador",
    df_team["Jugador"].sort_values().unique()
)

df_j = df_team[df_team["Jugador"] == jugador].iloc[0]

# --------------------------------------------------
# BLOQUE 1: USO Y CONFIANZA CT
# --------------------------------------------------
st.markdown("## 🧠 Uso y confianza del CT")
st.caption(
    "Describe qué tan recurrente es el uso del jugador por el entrenador. "
    "No evalúa calidad, solo decisiones."
)

st.dataframe(pd.DataFrame({
    "Métrica": [
        "Convocados",
        "Partidos jugados",
        "Partidos titular",
        "% Titularidad real",
        "Minutos por convocatoria",
        "Confianza CT"
    ],
    "Valor": [
        df_j["Convocados"],
        df_j["Partidos_Jugados"],
        df_j["Partidos_Titular"],
        round(df_j["Pct_Titularidad_Real"], 2),
        round(df_j["Minutos_por_Convocatoria"], 1),
        df_j["Confianza_CT"]
    ]
}))

# --------------------------------------------------
# BLOQUE 2: IMPACTO EN CANCHA
# --------------------------------------------------
st.markdown("## 📊 Impacto en cancha")
st.caption(
    "Evalúa producción ofensiva en relación a los minutos jugados."
)

st.dataframe(pd.DataFrame({
    "Métrica": [
        "Minutos",
        "Partidos 90",
        "Goles",
        "Goles por 90",
        "Impacto ofensivo",
        "Rank impacto (equipo)"
    ],
    "Valor": [
        df_j["Minutos"],
        round(df_j["Partidos_90"], 2),
        df_j["Goles"],
        round(df_j["Goles_p90"], 2),
        round(df_j["Impacto_Ofensivo"], 2),
        df_j["Rank_Impacto_Ofensivo"]
    ]
}))

# --------------------------------------------------
# BLOQUE 3: DISCIPLINA Y RIESGO
# --------------------------------------------------
st.markdown("## 🟨 Disciplina y riesgo")
st.caption(
    "Mide el comportamiento competitivo y el riesgo de sanciones."
)

st.dataframe(pd.DataFrame({
    "Métrica": [
        "Amarillas",
        "Rojas",
        "Tarjetas totales",
        "Tarjetas por 90",
        "Disciplina",
        "Jugador problema",
        "Rank disciplina (equipo)"
    ],
    "Valor": [
        df_j["Amarillas"],
        df_j["Rojas"],
        df_j["Tarjetas_Totales"],
        round(df_j["Tarjetas_p90"], 2),
        round(df_j["Disciplina"], 2),
        df_j["Jugador_Problema"],
        df_j["Rank_Disciplina"]
    ]
}))

# --------------------------------------------------
# BLOQUE 4: PESO EN EL EQUIPO
# --------------------------------------------------
st.markdown("## ⚖️ Peso en el equipo")
st.caption(
    "Refleja la importancia estructural del jugador dentro del equipo."
)

st.dataframe(pd.DataFrame({
    "Métrica": [
        "Peso en el equipo",
        "Rank peso (equipo)",
        "Minutos jugados"
    ],
    "Valor": [
        round(df_j["Peso_Equipo"], 2),
        df_j["Rank_Peso_Equipo"],
        df_j["Minutos"]
    ]
}))

