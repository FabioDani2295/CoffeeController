import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Titolo dell'app
st.title("📊 Dashboard Interattiva con Streamlit")

# Generare dati casuali
st.sidebar.header("Impostazioni del grafico")
num_points = st.sidebar.slider("Numero di punti", min_value=10, max_value=1000, value=100)

data = pd.DataFrame({
    "x": np.linspace(0, 10, num_points),
    "y": np.sin(np.linspace(0, 10, num_points)) + np.random.normal(scale=0.2, size=num_points)
})

# **Grafico Matplotlib**
st.subheader("📌 Grafico con Matplotlib")
fig, ax = plt.subplots()
ax.plot(data["x"], data["y"], label="Seno + Rumore", color='blue')
ax.legend()
st.pyplot(fig)

# **Grafico con Plotly**
st.subheader("📌 Grafico Interattivo con Plotly")
fig_plotly = px.scatter(data, x="x", y="y", title="Grafico Interattivo")
st.plotly_chart(fig_plotly)

# **Mostrare i dati**
st.subheader("📄 Anteprima dei dati")
st.write(data.head())
