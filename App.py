import streamlit as st
import Charts
import Data

st.set_page_config(page_title="📊 Environmental Dashboard", page_icon="🌍", layout="wide")

# **Mostrare l'Immagine in Alto**
st.image("ImageData.jpg", caption="📸 Analisi Ambientale", use_container_width=False)

# **Caricare i dati**
df = Data.load_data()

# **Mostrare la dashboard con grafici**
Charts.display_charts(df)

st.markdown("---")

