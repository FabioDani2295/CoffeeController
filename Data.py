import pandas as pd


# Caricamento dati da CSV
def load_data():
    file_path = "CoffeStatistics.csv"  # Assicurati che il file sia caricato nella directory corretta
    df = pd.read_csv(file_path)
    return df
