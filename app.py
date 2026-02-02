import streamlit as st
import pandas as pd

from utils.load_data import load_df, get_team_logos
from utils.ui import team_selector

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
