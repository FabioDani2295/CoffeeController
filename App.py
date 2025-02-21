import streamlit as st

st.title("La mia prima app con Streamlit!")
st.write("Benvenuto nella mia applicazione web interattiva.")

# Upload di file
uploaded_file = st.file_uploader("Carica un file CSV", type="csv")
if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.write(df.head())

print("procdiovedi questo secondo commit?")