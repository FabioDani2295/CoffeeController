import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

def display_charts(df):
    st.markdown("### 📊 Analisi delle Vendite di Caffè")

    col1, col2 = st.columns(2)

    # **Grafico Matplotlib**
    with col1:
        st.subheader("📌 Vendite per Tipo di Caffè")
        fig, ax = plt.subplots(figsize=(6,4))
        df.groupby("CoffeeType")["Sales (€)"].sum().plot(kind="bar", color="brown", ax=ax)
        ax.set_ylabel("Vendite (€)")
        ax.set_xlabel("Tipo di Caffè")
        ax.grid(True, linestyle="--", alpha=0.7)
        st.pyplot(fig)

    # **Grafico Plotly Interattivo**
    with col2:
        st.subheader("📌 Vendite Giorno per Giorno")
        fig_plotly = px.line(df, x="Date", y="Sales (€)", color="CoffeeType", title="Andamento Vendite")
        fig_plotly.update_layout(template="plotly_dark")
        st.plotly_chart(fig_plotly, use_container_width=True)

    # **Mostrare i dati grezzi se selezionato**
    if "show_data" in df and df["show_data"].all():
        st.subheader("📄 Dati Grezzi")
        st.dataframe(df.style.format("{:.2f}"))
