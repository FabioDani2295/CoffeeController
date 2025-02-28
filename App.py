import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

try:
    import pytz
    from streamlit_autorefresh import st_autorefresh

    HAS_EXTRAS = True
except ImportError:
    HAS_EXTRAS = False
    st.warning("Missing some optional dependencies. Install with: pip install pytz streamlit-autorefresh")

# Page configuration
st.set_page_config(
    page_title="☕ Coffee Assessment Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }
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
    [data-testid="stMetric"] > div:first-child {
        color: black !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)


# Load data function
@st.cache_data(ttl=30)
def load_data():
    try:
        csv_url = "https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/CoffeStatistics.csv"
        df = pd.read_csv(csv_url)
        df['Sample ID'] = range(1, len(df) + 1)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Create a dummy dataframe
        return pd.DataFrame()


# Set up auto-refresh if available
if HAS_EXTRAS:
    refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 5, 120, 30, 5)
    st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")

# Load the data
df = load_data()

# MAIN DASHBOARD
st.markdown('<div class="main-header">☕ Coffee Assessment Analysis</div>', unsafe_allow_html=True)

if not df.empty:
    # Get the latest coffee sample
    latest_sample = df.iloc[-1]

    st.markdown('<div class="section-header">Latest Coffee Sample Assessment</div>', unsafe_allow_html=True)

    # Sample header
    st.markdown(
        f'<h4 style="color: white; background-color: #333; padding: 5px; border-radius: 5px;">Sample #{len(df)}</h4>',
        unsafe_allow_html=True)

    # Create a row of metrics
    metrics = [
        ("Max Temp", "Max Temperature (°C)", "°C"),
        ("Mean Temp", "Mean Temperature (°C)", "°C"),
        ("PM2.5", "PM2_5_CU", ""),
        ("Particles >0.3μm", "particles_beyond_0_3", "")
    ]

    cols = st.columns(len(metrics))

    for i, (label, col_name, unit) in enumerate(metrics):
        if col_name in df.columns:
            with cols[i]:
                value = latest_sample[col_name]
                if len(df) > 1:
                    avg_prev = df.iloc[:-1][col_name].mean()
                    diff = value - avg_prev
                    st.metric(label, f"{value:.1f}{unit}", f"{diff:+.1f}{unit}")

                    # Color the delta value
                    color = "#FF4B4B" if diff < 0 else "#0CBA70"
                    st.markdown(f"""
                    <style>
                        div.stMetric:nth-child({i + 1}) [data-testid="stMetricDelta"] > div {{
                            color: {color} !important;
                            font-weight: bold !important;
                        }}
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    st.metric(label, f"{value:.1f}{unit}")

    # Display image and radar chart
    col1, col2 = st.columns([1, 2])

    with col1:
        # RGB display
        if all(col in df.columns for col in ['Mean_Red', 'Mean_Green', 'Mean_Blue']):
            r, g, b = int(latest_sample['Mean_Red']), int(latest_sample['Mean_Green']), int(latest_sample['Mean_Blue'])
            st.markdown(
                f"""
                <div style="width:100%; height:30px; background-color:rgb({r},{g},{b}); border-radius:5px;"></div>
                <div style="color:white;">RGB: {r}, {g}, {b}</div>
                """,
                unsafe_allow_html=True
            )

        # Coffee image
        try:
            st.image("ImageData.jpg", caption="Coffee Sample", use_container_width=True)
        except:
            st.info("Coffee image not available")

    with col2:
        if len(df) > 1:
            # Radar chart metrics
            radar_metrics = [
                "Max Temperature (°C)",
                "PM1_0_CU",
                "PM2_5_CU",
                "PM10_CU",
                "Max Value",
                "Mean_Red",
                "Mean_Green",
                "Mean_Blue"
            ]
            radar_metrics = [m for m in radar_metrics if m in df.columns]

            if radar_metrics:
                # Calculate averages and normalize
                avg_previous = df.iloc[:-1][radar_metrics].mean()
                max_values = df[radar_metrics].max()
                min_values = df[radar_metrics].min()
                range_values = max_values - min_values
                range_values = range_values.replace(0, 1)

                latest_normalized = (latest_sample[radar_metrics] - min_values) / range_values
                avg_normalized = (avg_previous - min_values) / range_values

                # Create radar chart
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=avg_normalized.values,
                    theta=radar_metrics,
                    fill='toself',
                    name='Average Previous',
                    line=dict(color='rgba(135, 206, 250, 0.7)'),
                ))
                fig.add_trace(go.Scatterpolar(
                    r=latest_normalized.values,
                    theta=radar_metrics,
                    fill='toself',
                    name='Latest Sample',
                    line=dict(color='rgba(255, 99, 71, 0.8)'),
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=True,
                    legend=dict(orientation="h", y=-0.1, x=0.5),
                    height=400,
                    font=dict(color="black")
                )
                st.plotly_chart(fig, use_container_width=True)

    # Raw data
    with st.expander("View Raw Data"):
        st.dataframe(df, use_container_width=True)

else:
    st.warning("No data available. Please check your connection.")

# Footer
footer_time = datetime.now()
if HAS_EXTRAS:
    rome_tz = pytz.timezone('Europe/Rome')
    footer_time = datetime.now(rome_tz)

st.markdown(f"""
<div style="text-align:center; color:#666; font-size:0.8rem;">
    Last updated: {footer_time.strftime('%Y-%m-%d %H:%M:%S')} | Total Samples: {len(df)}
</div>
""", unsafe_allow_html=True)