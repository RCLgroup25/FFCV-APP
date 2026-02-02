import streamlit as st


def team_selector(team_logos, cols=6):
    """
    Selector visual de equipos mediante logos.
    Guarda el equipo en session_state.
    """
    if "equipo_seleccionado" not in st.session_state:
        st.session_state.equipo_seleccionado = None

    st.markdown("### 🏟️ Selecciona un equipo")

    teams = list(team_logos.keys())
    rows = [teams[i:i + cols] for i in range(0, len(teams), cols)]

    for row in rows:
        columns = st.columns(cols)
        for col, team in zip(columns, row):
            with col:
                st.image(team_logos[team], use_container_width=True)

                if st.button(
                    team,
                    key=f"btn_{team}",
                    use_container_width=True
                ):
                    st.session_state.equipo_seleccionado = team

    return st.session_state.equipo_seleccionado
