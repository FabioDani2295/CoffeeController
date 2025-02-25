import streamlit as st
import Charts
import Data
from streamlit_autorefresh import st_autorefresh  # Import per l'aggiornamento automatico

st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

st_autorefresh(interval=10 * 1000, key="data_refresh")  # 10 secondi (10 * 1000 ms)

# **Caricare i dati**
df = Data.load_data()

# **Mostrare la dashboard con grafici**
Charts.display_charts(df)
st.markdown("---")
# **Mostrare immagine
st.image("ImageData.jpg", caption="📸 Analisi Ambientale dio amore", use_container_width=False)



