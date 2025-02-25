import pandas as pd
import time

# 📌 URL del file CSV su GitHub con timestamp per evitare cache
def load_data():
    timestamp = int(time.time())  # Cambia ogni secondo
    csv_url = f"https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/CoffeStatistics.csv?{timestamp}"
    return pd.read_csv(csv_url)

#da google: (possibile altro approccio)
"""
import pandas as pd

# 📌 Usa il tuo Google Sheet ID
gsheet_id = "1EozAS_K0kOUpmkLJc2QkMz32KLjqe8_VI5LSdySgNyw"
gsheet_url = f"https://docs.google.com/spreadsheets/d/{gsheet_id}/gviz/tq?tqx=out:csv"

def load_data():
    return pd.read_csv(gsheet_url)  # 🔄 Streamlit ora legge sempre i dati aggiornati da Google Sheets

"""

