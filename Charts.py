import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


def display_charts(df):
    st.markdown("### 📊 Visualizzazione Grafica")

    col1, col2 = st.columns(2)  # Creiamo due colonne

    with col1:
        st.subheader("📌 Grafico Matplotlib")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(df["x"], df["y"], color='blue', linestyle='-', marker='o', label="Seno + Rumore")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

    with col2:
        st.subheader("📌 Grafico Interattivo con Plotly")
        fig_plotly = px.scatter(df, x="x", y="y", title="Grafico Interattivo")
        st.plotly_chart(fig_plotly, use_container_width=True)
