import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

def display_charts(df):
    st.markdown("### 📊 Analisi dei Dati")

    # Creare due colonne per organizzare i grafici
    col1, col2 = st.columns(2)

    # **Grafico 1: Max Temperature (°C)**
    with col1:
        st.subheader("🌡 Massima Temperatura (°C)")
        fig_temp = px.line(df, x=df.index, y="Max Temperature (°C)", title="Andamento della Temperatura")
        st.plotly_chart(fig_temp, use_container_width=True)

    # **Grafico 2: PM1_0_CU**
    with col2:
        st.subheader("🌫 Concentrazione di PM1_0_CU")
        fig_pm = px.line(df, x=df.index, y="PM1_0_CU", title="Andamento del Particolato Fine (PM1_0)")
        st.plotly_chart(fig_pm, use_container_width=True)

    # **Grafico 3: **
    st.subheader("📊 Volume Caffe")
    fig_max = px.histogram(df, x="Max Value", title="Distribuzione dei Valori Massimi")
    st.plotly_chart(fig_max, use_container_width=True)
