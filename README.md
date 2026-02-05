🏟️ RCL Scout Group: Intelligence Platform (FFCV Grupo 4)

📊 Descripción del Proyecto

Esta plataforma es una herramienta avanzada de Business Intelligence aplicada al fútbol regional. No se limita a mostrar estadísticas básicas; calcula el peso específico y el impacto real de cada jugador dentro de la estructura de su equipo.

Diseñada específicamente para la 1ª Regional FFCV (Grupo 4), permite a directores técnicos y analistas identificar patrones de confianza del cuerpo técnico y riesgos disciplinarios de manera inmediata.

🧠 Ingeniería de Datos y Métricas Avanzadas

Lo que separa a esta app de un simple Excel es el cálculo de KPIs personalizados desarrollados mediante Python:

Peso en el Equipo: Un índice calculado que determina la importancia jerárquica de un jugador en la plantilla basándose en su participación y minutos clave.

Impacto Ofensivo Real: Métrica normalizada que evalúa la producción de goles ajustada por cada 90 minutos de juego efectivo.

Índice de Confianza (Uso del CT): Análisis de la relación entre convocatorias y titularidades reales para medir la "dependencia" que tiene el entrenador de ciertos perfiles.

Factor de Riesgo Disciplinario: Cálculo de tarjetas por cada 90 minutos, permitiendo predecir posibles sanciones antes de que ocurran.

🛠️ Stack Tecnológico

Streamlit: Framework para la entrega de datos en tiempo real con una interfaz fluida.

Pandas: Motor de transformación de datos (Data Wrangling) para la normalización de porcentajes y limpieza de posiciones.

Session State Management: Implementación de lógica de navegación interna para una experiencia de usuario (UX) sin recargas innecesarias.

Data Export Engine: Funcionalidad de exportación dinámica para que los usuarios puedan llevarse los datos filtrados a herramientas de video-análisis o informes impresos.


🖥️ Funcionalidades Master

Selector de Escudos Dinámico: Interfaz visual intuitiva para navegar entre los clubes del Grupo 4 (Villena CF, Novelda CF, Santa Pola CF, etc.).

Filtro de Minutos Global: Herramienta de limpieza para eliminar el "ruido estadístico" de jugadores con poca participación.

Ficha 360° del Jugador: Cuatro paneles de análisis profundo:

Uso y Confianza: ¿Cuánto confía realmente el DT en este jugador?

Impacto en Cancha: Productividad neta.

Disciplina y Riesgo: Semáforo de tarjetas.

Peso Jerárquico: Ranking dentro del plantel.
