import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configurazione della pagina: DEVE ESSERE LA PRIMA chiamata Streamlit
st.set_page_config(
    page_title="☕ Coffee Assessment Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Definire una funzione per iniettare il CSS personalizzato
def inject_css():
    st.markdown("""
    <style>
        /* Cambia il colore del testo delle metriche in nero */
        div[data-testid="stMetricLabel"] {
            color: black !important;
            font-weight: bold;
        }
        div[data-testid="stMetricValue"] {
            color: black !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)


def inject_compact_css():
    st.markdown("""
    <style>
        /* Ensure high contrast for all text elements */
        .stApp {
            background-color: #1E1E1E;
        }
        /* More compact design with CamelCase */
        .main-header {
            font-size: 1.8rem;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-bottom: 0.5rem;
            text-transform: capitalize;
        }
        .section-header {
            color: white;
            font-size: 1.2rem;
            margin-top: 0.5rem;
            margin-bottom: 0.3rem;
            text-transform: capitalize;
        }
        /* High contrast metrics styling with black labels */
        [data-testid="stMetric"] {
            background-color: white;
            padding: 0.5rem;
            border-radius: 0.3rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            margin-bottom: 0.5rem;
        }
        /* Make metric labels (titles) black for visibility */
        [data-testid="stMetric"] > div:first-child {
            font-size: 0.9rem !important;
            color: black !important;
            font-weight: bold;
            background-color: #f0f0f0;
            padding: 3px 5px;
            border-radius: 3px;
        }
        /* Main metric value */
        [data-testid="stMetric"] > div:nth-child(2) {
            font-size: 1.2rem !important;
            color: #000 !important;
        }
        /* Container for delta values */
        [data-testid="stMetricDelta"] {
            background-color: rgba(250, 250, 250, 0.9);
            padding: 2px 5px;
            border-radius: 3px;
        }
        /* Hide the default delta arrow */
        [data-testid="stMetricDelta"] svg {
            display: none !important;
        }
        /* Make the text smaller */
        .small-font {
            font-size: 0.9rem;
        }
        /* Reduce spacing */
        div.block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        /* Customize sidebar */
        .css-1d391kg, .css-1lcbmhc {
            padding-top: 1rem;
        }
        /* Dataframe styling */
        .dataframe-container {
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)


# Map new column names to expected names in the app
def map_column_names(df):
    """Map the new column names from process_images to the expected column names in the app"""
    column_mapping = {
        'mean_H': 'Mean_H',
        'mean_S': 'Mean_S',
        'mean_a': 'a*',
        'mean_b': 'b*',
        'dom_R': 'Mean_Red',
        'dom_G': 'Mean_Green',
        'dom_B': 'Mean_Blue'
    }

    # Create a copy of the dataframe
    df_mapped = df.copy()

    # Rename columns based on mapping
    for new_col, old_col in column_mapping.items():
        if new_col in df_mapped.columns:
            df_mapped.rename(columns={new_col: old_col}, inplace=True)

    return df_mapped


if __name__ == "__main__":
    # Iniettare il CSS personalizzato dopo la configurazione della pagina
    inject_css()
    inject_compact_css()


    # Funzione per il caricamento dei dati
    @st.cache_data(ttl=30)  # Cache dei dati per 30 secondi
    def load_data():
        timestamp = int(time.time())
        try:
            csv_url = f"https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/CoffeStatistics.csv?{timestamp}"
            df = pd.read_csv(csv_url)
            # Aggiunge una colonna "Sample ID" per il tracciamento
            df['Sample ID'] = range(1, len(df) + 1)
            # Map new column names to old ones
            df = map_column_names(df)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            # Restituisce dati di esempio se il caricamento fallisce
            df = pd.read_csv("CoffeStatistics.csv") if st.session_state.get("demo_mode", False) else pd.DataFrame()
            df = map_column_names(df)
            return df


    # Inizializzazione dello stato di sessione per le selezioni
    if 'selected_metrics' not in st.session_state:
        st.session_state.selected_metrics = {
            'temperature': ['Max Temperature (°C)', 'Mean Temperature (°C)'],
            'particulate': ['PM1_0_CU', 'PM2_5_CU', 'PM10_CU'],
            'color': ['Mean_Red', 'Mean_Green', 'Mean_Blue'],
            'particles': ['particles_beyond_0_3', 'particles_beyond_1_0']
        }

    if 'refresh_rate' not in st.session_state:
        st.session_state.refresh_rate = 30

    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False

    # Auto-refresh basato sullo stato di sessione
    refresh_count = st_autorefresh(interval=st.session_state.refresh_rate * 1000, key="data_refresh")

    # Caricamento dei dati
    df = load_data()

    # SIDEBAR - Design più compatto
    with st.sidebar:
        st.markdown("### ⚙️ Dashboard Controls")

        # Controllo del refresh rate
        st.slider(
            "Refresh Rate (sec)",
            min_value=5,
            max_value=120,
            value=st.session_state.refresh_rate,
            step=5,
            key="refresh_rate_input",
            on_change=lambda: setattr(st.session_state, 'refresh_rate', st.session_state.refresh_rate_input)
        )

        # Toggle per Demo Mode
        st.checkbox(
            "Demo Mode",
            value=st.session_state.demo_mode,
            key="demo_mode_input",
            on_change=lambda: setattr(st.session_state, 'demo_mode', st.session_state.demo_mode_input),
            help="Use local data if online source unavailable"
        )

        # Organizzazione delle colonne per categoria, aggiornata
        column_categories = {
            "Temperature": [col for col in df.columns if "Temperature" in col],
            "Particulate Matter": [col for col in df.columns if "PM" in col],
            "Particles": [col for col in df.columns if "particles_beyond" in col],
            "Color": ['Mean_Red', 'Mean_Green', 'Mean_Blue', 'Mean_H', 'Mean_S', 'a*', 'b*', 'Dist_White', 'Dist_Gray'],
            "Weight": ['Min Weight', 'Max Weight', 'Weight Range', 'Average Weight']
        }

        # Selezione delle metriche nella sidebar
        st.markdown("### 📊 Metrics")
        selected_metrics = {}

        # Per ogni categoria, viene creato un multiselect
        for category, columns in column_categories.items():
            # Filter out columns that don't exist in df
            available_columns = [col for col in columns if col in df.columns]
            if available_columns:  # Mostra solo le categorie con colonne
                default_selection = [col for col in
                                     st.session_state.selected_metrics.get(category, available_columns[:2]) if
                                     col in available_columns]
                selected_metrics[category] = st.multiselect(
                    f"{category}",
                    options=available_columns,
                    default=default_selection,
                    key=f"select_{category}"
                )
                # Aggiorna lo stato di sessione
                st.session_state.selected_metrics[category] = selected_metrics[category]

    # DASHBOARD PRINCIPALE
    st.markdown('<div class="main-header">☕ Coffee Assessment Analysis</div>', unsafe_allow_html=True)

    # CONFRONTO ULTIMO CAMPIONE DI COFFEE
    if not df.empty:
        # Recupera l'ultimo campione (ultima riga) e i campioni precedenti
        latest_sample = df.iloc[-1]

        st.markdown('<div class="section-header">Latest Coffee Sample Assessment</div>', unsafe_allow_html=True)

        # Visualizzazione del Sample ID
        st.markdown(
            '<h4 style="color: white; background-color: #333; padding: 5px; border-radius: 5px;">Sample #{}</h4>'.format(
                len(df)), unsafe_allow_html=True)

        # Visualizzazione compatta delle metriche per l'ultimo campione
        key_metrics = [
            ("Max Temp", "Max Temperature (°C)", "°C"),
            ("Mean Temp", "Mean Temperature (°C)", "°C"),
            ("PM2.5", "PM2_5_CU", ""),
            ("Particles >0.3μm", "particles_beyond_0_3", "")
        ]

        # Creazione di una riga di metriche
        metric_cols = st.columns(len(key_metrics))

        for i, (label, col_name, unit) in enumerate(key_metrics):
            if col_name in df.columns:
                with metric_cols[i]:
                    value = latest_sample[col_name]
                    if len(df) > 1:
                        avg_prev = df.iloc[:-1][col_name].mean()
                        diff = value - avg_prev
                        if diff < 0:
                            diff_html = f'<span style="color: #ff4b4b; font-weight: bold;">{diff:+.1f}{unit} vs avg</span>'
                        else:
                            diff_html = f'<span style="color: #28a745; font-weight: bold;">{diff:+.1f}{unit} vs avg</span>'
                        st.metric(
                            label,
                            f"{value:.1f}{unit}",
                            delta=None
                        )
                        st.markdown(diff_html, unsafe_allow_html=True)
                    else:
                        st.metric(label, f"{value:.1f}{unit}")

        # Creazione di due colonne per immagine/color e grafico radar
        col1, col2 = st.columns([1, 2])

        with col1:
            if all(col in df.columns for col in ['Mean_Red', 'Mean_Green', 'Mean_Blue']):
                r, g, b = int(latest_sample['Mean_Red']), int(latest_sample['Mean_Green']), int(
                    latest_sample['Mean_Blue'])
                st.markdown(
                    f"""
                    <div style="
                        width: 100%; 
                        height: 30px; 
                        background-color: rgb({r},{g},{b}); 
                        border-radius: 5px;
                        margin-top: 10px;
                        margin-bottom: 5px;
                    "></div>
                    <div style="color:white; font-size:0.9rem;">RGB: {r}, {g}, {b}</div>
                    """,
                    unsafe_allow_html=True
                )
            try:
                st.image("ImageData.jpg", caption="Latest Coffee Sample Image", use_container_width=True)
            except Exception as e:
                st.warning(f"Coffee image not available: {e}")

        # Replace the existing radar chart code in the with col2: section
        with col2:
            if len(df) > 1:
                # Exactly the metrics you requested
                radar_metrics = [
                    "Max Temperature (°C)",
                    "PM1_0_CU",
                    "PM2_5_CU",
                    "Average Weight",
                    "Mean_H",
                    "Mean_S"
                ]

                # Filter to only metrics that exist in the dataframe
                radar_metrics = [m for m in radar_metrics if m in df.columns]

                if radar_metrics:
                    # Calculate statistics for normalization
                    avg_previous = df.iloc[:-1][radar_metrics].mean()

                    # Get min and max values for scaling per metric
                    max_values = df[radar_metrics].max()
                    min_values = df[radar_metrics].min()

                    # Calculate range while avoiding division by zero
                    range_values = max_values - min_values
                    range_values = range_values.replace(0, 1)  # Avoid division by zero

                    # Normalize values to 0-1 scale (0-100%)
                    latest_normalized = (latest_sample[radar_metrics] - min_values) / range_values
                    avg_normalized = (avg_previous - min_values) / range_values

                    # Create radar chart
                    fig = go.Figure()

                    # Add average of previous samples
                    fig.add_trace(go.Scatterpolar(
                        r=avg_normalized.values,
                        theta=radar_metrics,
                        fill='toself',
                        name='Average Previous',
                        line=dict(color='rgba(135, 206, 250, 0.7)'),
                    ))

                    # Add latest sample
                    fig.add_trace(go.Scatterpolar(
                        r=latest_normalized.values,
                        theta=radar_metrics,
                        fill='toself',
                        name='Latest Sample',
                        line=dict(color='rgba(255, 99, 71, 0.8)'),
                    ))

                    # Update layout with simplified settings
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1],
                                tickvals=[0, 0.25, 0.5, 0.75, 1],
                                ticktext=['0%', '25%', '50%', '75%', '100%']
                            )
                        ),
                        showlegend=False,  # No legend as requested
                        margin=dict(l=30, r=30, t=20, b=30),
                        height=440,
                        font=dict(color="white")
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Add a simple note about normalization
                    st.markdown("""
                    <div style="background-color: rgba(50, 50, 50, 0.7); padding: 8px; border-radius: 5px; font-size: 0.8rem; color: white; margin-top: -15px; text-align: center;">
                    Each axis normalized 0-100% for proper comparison
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Some of the requested metrics are not available in the data")
            else:
                st.info("Only one sample available. More samples needed for comparison.")

        tabs = st.tabs([
            "Temperature",
            "Particulate",
            "Color",
            "Particles",
            "Weight"
        ])

        with tabs[0]:
            temp_metrics = selected_metrics.get("Temperature", [])
            if temp_metrics:
                fig = px.line(
                    df,
                    x="Sample ID",
                    y=temp_metrics,
                    markers=True,
                    line_shape="spline",
                    height=280
                )
                fig.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                    margin=dict(l=20, r=20, t=10, b=40),
                    xaxis=dict(tickmode='linear', dtick=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Select temperature metrics in the sidebar")

        with tabs[1]:
            pm_metrics = selected_metrics.get("Particulate Matter", [])
            if pm_metrics:
                fig = px.line(
                    df,
                    x="Sample ID",
                    y=pm_metrics,
                    markers=True,
                    line_shape="spline",
                    height=280
                )
                fig.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                    margin=dict(l=20, r=20, t=10, b=40),
                    xaxis=dict(tickmode='linear', dtick=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Select particulate metrics in the sidebar")

        with tabs[2]:
            color_metrics = selected_metrics.get("Color", [])
            if color_metrics and 'Mean_Red' in df.columns and 'Mean_Green' in df.columns and 'Mean_Blue' in df.columns:
                col1, col2 = st.columns([3, 1])
                with col1:
                    fig = px.line(
                        df,
                        x="Sample ID",
                        y=color_metrics,
                        markers=True,
                        line_shape="spline",
                        height=280
                    )
                    fig.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                        margin=dict(l=20, r=20, t=10, b=40),
                        xaxis=dict(tickmode='linear', dtick=1)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.markdown("#### Color Swatches")
                    for i in range(len(df)):
                        r, g, b = int(df.iloc[i]['Mean_Red']), int(df.iloc[i]['Mean_Green']), int(
                            df.iloc[i]['Mean_Blue'])
                        sample_id = i + 1
                        st.markdown(
                            f"""
                            <div style="display: flex; align-items: center; margin-bottom: 5px; font-size: 0.8rem;">
                                <div style="flex: 0 0 20px; margin-right: 5px;">#{sample_id}</div>
                                <div style="
                                    flex: 1;
                                    height: 15px; 
                                    background-color: rgb({r},{g},{b}); 
                                    border-radius: 3px;
                                "></div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("Select color metrics in the sidebar")

        with tabs[3]:
            particles_metrics = selected_metrics.get("Particles", [])
            if particles_metrics:
                fig = px.bar(
                    df,
                    x="Sample ID",
                    y=particles_metrics,
                    barmode="group",
                    height=280
                )
                fig.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                    margin=dict(l=20, r=20, t=10, b=40),
                    xaxis=dict(tickmode='linear', dtick=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Select particle metrics in the sidebar")

        with tabs[4]:
            values_metrics = selected_metrics.get("Values", [])
            if values_metrics:
                fig = px.line(
                    df,
                    x="Sample ID",
                    y=values_metrics,
                    markers=True,
                    line_shape="spline",
                    height=280
                )
                fig.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
                    margin=dict(l=20, r=20, t=10, b=40),
                    xaxis=dict(tickmode='linear', dtick=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Select value metrics in the sidebar")

        st.markdown('<div class="section-header">Statistical Analysis</div>', unsafe_allow_html=True)

        all_selected = []
        for metrics in selected_metrics.values():
            all_selected.extend(metrics)

        if len(all_selected) >= 2:
            corr = df[all_selected].corr()
            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                zmin=-1, zmax=1,
                height=600
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=30, b=10)
            )
            fig.update_traces(textfont=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least 2 metrics to view correlations")

        col1, col2 = st.columns(2)
        with col1:
            if len(df) > 1:
                rank_metrics = ["Max Temperature (°C)", "PM2_5_CU", "particles_beyond_0_3"]
                rank_metrics = [m for m in rank_metrics if m in df.columns]
                if rank_metrics:
                    percentile_ranks = {}
                    for metric in rank_metrics:
                        all_values = df[metric].sort_values().values
                        latest_value = latest_sample[metric]
                        percentile = sum(all_values < latest_value) / len(all_values) * 100
                        percentile_ranks[metric] = percentile
                    fig = px.bar(
                        x=list(percentile_ranks.keys()),
                        y=list(percentile_ranks.values()),
                        labels={'x': 'Metric', 'y': 'Percentile Rank'},
                        height=300,
                        text=[f"{p:.1f}%" for p in percentile_ranks.values()]
                    )
                    fig.update_layout(
                        margin=dict(l=10, r=10, t=30, b=10),
                        title="Latest Sample Percentile Rank",
                        yaxis=dict(range=[0, 100])
                    )
                    fig.update_traces(textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Key metrics not available for ranking")
            else:
                st.info("Need more samples for percentile ranking")
        with col2:
            st.write("")
        with st.expander("View Raw Data"):
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=200)
            st.markdown('</div>', unsafe_allow_html=True)
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"coffee_assessment_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )
    else:
        st.warning("No data available. Please check your connection or enable Demo Mode in the sidebar.")

    rome_tz = pytz.timezone('Europe/Rome')
    rome_time = datetime.now(rome_tz).strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"""
    <div style="text-align: center; font-size: 0.8rem; margin-top: 1rem; color: #666;">
        Last updated: {rome_time} (Rome Time) | Total Samples: {len(df)}
    </div>
    """, unsafe_allow_html=True)