import pandas as pd
import time

# 📌 URL del file CSV su GitHub con timestamp per evitare cache
def load_data():
    timestamp = int(time.time())  # Cambia ogni secondo
    csv_url = f"https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/CoffeStatistics.csv?{timestamp}"
    return pd.read_csv(csv_url)

