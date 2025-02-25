import streamlit as st


def show_sidebar():
    st.sidebar.header("🔧 Impostazioni Dashboard")

    # Selettore per filtrare il tipo di caffè
    coffee_type = st.sidebar.selectbox("Scegli il tipo di caffè", ["Tutti", "Espresso", "Americano", "Cappuccino"])

    # Slider per selezionare un range di vendite
    sales_range = st.sidebar.slider("Seleziona intervallo vendite (€)", min_value=0, max_value=1000, value=(100, 500))

    # Checkbox per visualizzare i dati grezzi
    show_data = st.sidebar.checkbox("Mostra tabella dati")

    return {"coffee_type": coffee_type, "sales_range": sales_range, "show_data": show_data}
