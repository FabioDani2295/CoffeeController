import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configurazione della pagina
st.set_page_config(
    page_title="📊 Dashboard Avanzata con Streamlit",
    page_icon="📈",
    layout="wide"

)

# Stile personalizzato con CSS
st.markdown("""
    <style>
        .main-title {
            font-size:40px !important;
            font-weight: bold;
            text-align: center;
            color: #4CAF50;
        }
        .sub-header {
            font-size:24px !important;
            font-weight: bold;
            color: #ff6347;
        }
    </style>
""", unsafe_allow_html=True)

# Titolo dell'app
st.markdown('<p class="main-title">📊 Dashboard Avanzata con Streamlit</p>', unsafe_allow_html=True)

# **Sidebar**
st.sidebar.header("🔧 Impostazioni")
num_points = st.sidebar.slider("Numero di punti", min_value=10, max_value=1000, value=100)
chart_type = st.sidebar.selectbox("📊 Scegli il tipo di grafico", ["Linea", "Scatter", "Barre"])
show_data = st.sidebar.checkbox("Mostra la tabella dati")

# **Generare dati casuali**
data = pd.DataFrame({
    "x": np.linspace(0, 10, num_points),
    "y": np.sin(np.linspace(0, 10, num_points)) + np.random.normal(scale=0.2, size=num_points)
})

# **Disposizione in colonne**
col1, col2 = st.columns(2)

# **Grafico Matplotlib**
with col1:
    st.markdown('<p class="sub-header">📌 Grafico Matplotlib</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 4))

    if chart_type == "Linea":
        ax.plot(data["x"], data["y"], color='blue', linestyle='-', marker='o', label="Seno + Rumore")
    elif chart_type == "Scatter":
        ax.scatter(data["x"], data["y"], color='red', label="Dati Dispersione")
    elif chart_type == "Barre":
        ax.bar(data["x"], data["y"], color='purple', label="Istogramma")

    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

# **Grafico Interattivo con Plotly**
with col2:
    st.markdown('<p class="sub-header">📌 Grafico Interattivo con Plotly</p>', unsafe_allow_html=True)
    if chart_type == "Linea":
        fig_plotly = px.line(data, x="x", y="y", title="Grafico Interattivo")
    elif chart_type == "Scatter":
        fig_plotly = px.scatter(data, x="x", y="y", title="Grafico Interattivo")
    elif chart_type == "Barre":
        fig_plotly = px.bar(data, x="x", y="y", title="Grafico Interattivo")

    fig_plotly.update_layout(template="plotly_dark")
    st.plotly_chart(fig_plotly, use_container_width=True)

# **Mostrare i dati**
if show_data:
    st.subheader("📄 Anteprima dei dati")
    st.dataframe(data.style.format("{:.2f}"))
