import streamlit as st
import Charts
import Data
from streamlit_autorefresh import st_autorefresh  # Import per aggiornamento automatico

# 📌 Configurazione della dashboard
st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

# 📌 **Aggiornamento automatico ogni 30 secondi**
st_autorefresh(interval=30 * 1000, key="data_refresh")

# 📌 **Caricare i dati aggiornati dal CSV**
df = Data.load_data()

# 📌 **Mostrare i grafici**
Charts.display_charts(df)

st.markdown("---")

# 📌 **Sezione: Visualizzazione dei Dati Grezzi**
st.subheader("📄 Dati Grezzi")
st.write(df)  # Mostra la tabella con i dati grezzi

# 📌 **Mostrare immagine**
st.image("ImageData.jpg", caption="📸 Analisi Ambientale", use_container_width=False)
