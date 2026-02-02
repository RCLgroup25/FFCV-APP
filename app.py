import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURACIÓN ÚNICA DE LA PÁGINA ---
st.set_page_config(page_title="RCL Scout Group - Scouting 2026", layout="wide")

# --- 2. FUNCIONES DE CARGA (LOAD DATA) ---
@st.cache_data
def load_df():
    # Intentamos cargar desde la carpeta data o desde la raíz
    for ruta in ["data/df.csv", "df.csv"]:
        if os.path.exists(ruta):
            return pd.read_csv(ruta)
    return None

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

# --- 3. INTERFAZ: SELECTOR DE EQUIPOS (CON KEY ÚNICA) ---
def team_selector(team_logos, cols=4):
    if "equipo_seleccionado" not in st.session_state:
        st.session_state.equipo_seleccionado = None

    st.markdown("### 🏟️ Selecciona un equipo")
    teams = list(team_logos.keys())
    columns = st.columns(cols)

    for i, team in enumerate(teams):
        col_idx = i % cols
        with columns[col_idx]:
            # Mostrar Logo
            try:
                st.image(team_logos[team], use_container_width=True)
            except:
                st.caption(f"📍 {team}")
            
            # BOTÓN CON KEY ÚNICA PARA EVITAR ERROR DuplicateElementKey
            if st.button(team, key=f"btn_{team}_{i}", use_container_width=True):
                st.session_state.equipo_seleccionado = team
                st.rerun()

    return st.session_state.equipo_seleccionado

# --- 4. EJECUCIÓN PRINCIPAL ---
st.title("⚽ RCL Scout Group: Inteligencia Grupo 4")
st.caption("Herramienta descriptiva para scouting y cuerpos técnicos.")

df = load_df()
team_logos = get_team_logos()

if df is None:
    st.error("No se encontró el archivo df.csv en 'data/' o en la raíz.")
    st.stop()

# --- FILTRO GLOBAL ---
st.sidebar.markdown("### ⏱️ Filtros")
min_minutos = st.sidebar.slider(
    "Minutos mínimos jugados",
    0, int(df["Minutos"].max()), 300, 50
)
df_filtrado = df[df["Minutos"] >= min_minutos]

# --- SELECTOR ---
equipo = team_selector(team_logos)

if equipo:
    st.divider()
    st.markdown(f"## 🏟️ {equipo}")
    df_team = df_filtrado[df_filtrado["Equipo"] == equipo]

    if df_team.empty:
        st.warning("No hay jugadores con ese filtro de minutos.")
    else:
        # TABLA GENERAL
        st.markdown("### 📋 Plantel del equipo")
        cols_mostrar = ["Jugador", "Posicion_Limpia", "Minutos", "Partidos_Jugados", 
                        "Pct_Titularidad_Real", "Goles", "Goles_p90", "Tarjetas_Totales"]
        st.dataframe(df_team[cols_mostrar].sort_values("Minutos", ascending=False), use_container_width=True)

        # SELECTOR DE JUGADOR
        st.markdown("### 👤 Análisis individual")
        jugador_sel = st.selectbox("Selecciona jugador", df_team["Jugador"].unique())
        
        if jugador_sel:
            df_j = df_team[df_team["Jugador"] == jugador_sel].iloc[0]

            # BLOQUES DE DATOS (Métricas)
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🧠 Uso y confianza CT")
                st.table(pd.DataFrame({
                    "Métrica": ["Convocados", "PJ", "Titular", "% Titul.", "Min/Conv", "Confianza CT"],
                    "Valor": [df_j["Convocados"], df_j["Partidos_Jugados"], df_j["Partidos_Titular"], 
                              f"{df_j['Pct_Titularidad_Real']}%", round(df_j["Minutos_por_Convocatoria"],1), df_j["Confianza_CT"]]
                }))

                st.subheader("🟨 Disciplina")
                st.table(pd.DataFrame({
                    "Métrica": ["Amarillas", "Rojas", "Tarjetas/90", "Disciplina", "Jugador Problema"],
                    "Valor": [df_j["Amarillas"], df_j["Rojas"], round(df_j["Tarjetas_p90"],2), 
                              round(df_j["Disciplina"],2), df_j["Jugador_Problema"]]
                }))

            with c2:
                st.subheader("📊 Impacto en cancha")
                st.table(pd.DataFrame({
                    "Métrica": ["Minutos", "Partidos 90", "Goles", "Goles p90", "Impacto Ofensivo"],
                    "Valor": [df_j["Minutos"], round(df_j["Partidos_90"],2), df_j["Goles"], 
                              round(df_j["Goles_p90"],2), round(df_j["Impacto_Ofensivo"],2)]
                }))

                st.subheader("⚖️ Peso en Equipo")
                st.table(pd.DataFrame({
                    "Métrica": ["Peso en Equipo", "Rank Peso", "Minutos Totales"],
                    "Valor": [round(df_j["Peso_Equipo"],2), df_j["Rank_Peso_Equipo"], df_j["Minutos"]]
                }))
