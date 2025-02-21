import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📂 Caricamento e Analisi di un CSV")

# Upload file
uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File caricato con successo!")

    # Mostra i dati
    st.subheader("📄 Anteprima dei dati")
    st.write(df.head())

    # Scelta colonna per istogramma
    column = st.selectbox("Seleziona una colonna per l'istogramma", df.columns)

    # Grafico istogramma
    st.subheader(f"📊 Istogramma di {column}")
    fig, ax = plt.subplots()
    df[column].hist(ax=ax, bins=20)
    st.pyplot(fig)
