import streamlit as st
import Charts
import Data

# Configurazione della pagina
st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

# Caricare i dati
df = Data.load_data()  # Nessun filtro, mostriamo tutti i dati

# Mostrare la dashboard con grafici
Charts.display_charts(df)

# Footer
st.markdown("---")
st.text("📌 Dashboard sviluppata con Streamlit")
