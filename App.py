import streamlit as st
import Charts
import Data
import time
from streamlit_autorefresh import st_autorefresh

# 📌 Configurazione della dashboard
st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

# 📌 **Aggiornamento automatico ogni 10 secondi**
st_autorefresh(interval=10 * 1000, key="data_refresh")

# 📌 **Forzare il ricaricamento dei dati**
st.write("🔄 Ultimo aggiornamento:", time.strftime("%H:%M:%S"))

df = Data.load_data()  # 📌 Adesso carica sempre i dati aggiornati

# 📌 **Sezione: Visualizzazione dei Dati Grezzi**
st.subheader("📄 Dati Grezzi")
st.write(df)  # Mostra la tabella con i dati grezzi

# 📌 **Mostrare i grafici**
Charts.display_charts(df)

st.markdown("---")

# 📌 **Mostrare immagine**
image_url = "https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/ImageData.jpg"
st.image(image_url, caption="📸 Analisi Ambientale", use_container_width=False)
