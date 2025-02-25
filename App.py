import streamlit as st
import Charts
import Data

# 📌 Configurazione della dashboard
st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

# 📌 **Bottone per forzare il refresh**
if st.button("🔄 Ricarica i dati"):
    st.cache_data.clear()  # Cancella la cache manualmente

# 📌 **Caricare i dati aggiornati dal CSV su GitHub**
df = Data.load_data()

# 📌 **Sezione: Visualizzazione dei Dati Grezzi**
st.subheader("📄 Dati Grezzi")
st.write(df)  # Mostra la tabella con i dati grezzi

# 📌 **Mostrare i grafici**
Charts.display_charts(df)

st.markdown("---")
