import streamlit as st
import SideBar
import Charts
import Data

# Configurazione della pagina
st.set_page_config(page_title="☕ Testing Coffee Dashboard", page_icon="📊", layout="wide")

# Sidebar
filters = SideBar.show_sidebar()

# Caricare i dati
df = Data.load_data()

# Applicare i filtri della sidebar
#filtered_df = Data.filter_data(df, filters)

# Mostrare la dashboard con grafici
#Charts.display_charts(filtered_df)

# Footer
st.markdown("---")
