import pandas as pd


# Caricamento dati da CSV
def load_data():
    file_path = "CoffeStatistics.csv"  # Assicurati che il file sia caricato nella directory corretta
    df = pd.read_csv(file_path)
    return df


# Applicazione filtri
def filter_data(df, filters):
    if filters["coffee_type"] != "Tutti":
        df = df[df["CoffeeType"] == filters["coffee_type"]]

    # Filtrare per vendite
    min_sales, max_sales = filters["sales_range"]
    df = df[(df["Sales (€)"] >= min_sales) & (df["Sales (€)"] <= max_sales)]

    return df
