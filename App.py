import streamlit as st
import Charts
import Data
from streamlit_autorefresh import st_autorefresh

# 📌 Configurazione della dashboard
st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

# 📌 **Forza il refresh della cache**
st.cache_data.clear()

# 📌 **Aggiornamento automatico ogni 10 secondi**
st_autorefresh(interval=10 * 1000, key="data_refresh")

# 📌 **Caricare i dati aggiornati dal CSV su GitHub**
df = Data.load_data()

# 📌 **Sezione: Visualizzazione dei Dati Grezzi**
st.subheader("📄 Dati Grezzi")
st.write(df)  # Mostra la tabella con i dati grezzi

# 📌 **Mostrare i grafici**
Charts.display_charts(df)

st.markdown("---")
