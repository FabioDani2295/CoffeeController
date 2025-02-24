import streamlit as st
import SideBar  # Modulo personalizzato per la sidebar
import Charts   # Modulo per i grafici
import Data    # Modulo per la gestione dati

# Configurazione della pagina
st.set_page_config(page_title="📊 Dashboard", page_icon="📈", layout="wide")

# Sidebar
SideBar.show_sidebar()

# Caricare i dati
df = Data.load_data()

# Mostrare i grafici
Charts.display_charts(df)

# Footer
st.markdown("---")
st.text("📌 Dashboard sviluppata con Streamlit")
