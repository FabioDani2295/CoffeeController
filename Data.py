import pandas as pd
import streamlit as st

# 📌 URL del file CSV su GitHub
csv_url = "https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/CoffeStatistics.csv"

@st.cache_data(ttl=10)  # Cache aggiornata ogni 10 secondi
def load_data():
    df = pd.read_csv(csv_url)
    return df
