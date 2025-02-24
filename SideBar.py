import streamlit as st


def show_sidebar():
    st.sidebar.header("🔧 Impostazioni")

    # Slider per il numero di punti
    num_points = st.sidebar.slider("Numero di punti", min_value=10, max_value=1000, value=100)

    # Selettore per il tipo di grafico
    chart_type = st.sidebar.selectbox("📊 Scegli il tipo di grafico", ["Linea", "Scatter", "Barre"])

    # Checkbox per mostrare/nascondere i dati
    show_data = st.sidebar.checkbox("Mostra la tabella dati")

    return num_points, chart_type, show_data
