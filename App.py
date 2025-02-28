import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="☕ Coffee Environmental Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3d2c1d;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #5e4632;
        margin-top: 1rem;
    }
    .metric-container {
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .highlight {
        color: #c25e00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Load data function
@st.cache_data(ttl=30)  # Cache data for 30 seconds
def load_data():
    timestamp = int(time.time())
    try:
        csv_url = f"https://raw.githubusercontent.com/FabioDani2295/CoffeeController/main/CoffeStatistics.csv?{timestamp}"
        df = pd.read_csv(csv_url)
        # Add a sequence column for tracking measurements
        df['Sequence'] = range(1, len(df) + 1)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Return sample data if loading fails
        return pd.read_csv("CoffeStatistics.csv") if st.session_state.get("demo_mode", False) else pd.DataFrame()


# Initialize session state for selections
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

# Auto-refresh based on session state
refresh_count = st_autorefresh(interval=st.session_state.refresh_rate * 1000, key="data_refresh")

# Load the data
df = load_data()

# SIDEBAR
st.sidebar.markdown("## ⚙️ Dashboard Controls")

# Refresh rate control
st.sidebar.slider(
    "Refresh Rate (seconds)",
    min_value=5,
    max_value=120,
    value=st.session_state.refresh_rate,
    step=5,
    key="refresh_rate_input",
    on_change=lambda: setattr(st.session_state, 'refresh_rate', st.session_state.refresh_rate_input)
)

# Demo mode toggle
st.sidebar.checkbox(
    "Demo Mode (use local file)",
    value=st.session_state.demo_mode,
    key="demo_mode_input",
    on_change=lambda: setattr(st.session_state, 'demo_mode', st.session_state.demo_mode_input)
)

# Organize columns by category
column_categories = {
    "Temperature Metrics": [col for col in df.columns if "Temperature" in col],
    "Particulate Matter": [col for col in df.columns if "PM" in col],
    "Particle Size Distribution": [col for col in df.columns if "particles_beyond" in col],
    "Color Metrics": ['Mean_Red', 'Mean_Green', 'Mean_Blue', 'L*', 'a*', 'b*', 'Dist_White', 'Dist_Gray'],
    "Value Metrics": ['Min Value', 'Max Value', 'Range', 'Mean']
}

# Sidebar metric selection
st.sidebar.markdown("## 📊 Metric Selection")
selected_metrics = {}

# For each category, create a multiselect
for category, columns in column_categories.items():
    if columns:  # Only show categories with columns
        default_selection = st.session_state.selected_metrics.get(category, columns[:2])
        selected_metrics[category] = st.sidebar.multiselect(
            f"Select {category}",
            options=columns,
            default=default_selection
        )
        # Update session state
        st.session_state.selected_metrics[category] = selected_metrics[category]

# MAIN DASHBOARD
st.markdown('<div class="main-header">☕ Coffee Environmental Monitoring Dashboard</div>', unsafe_allow_html=True)

# KEY METRICS ROW
if not df.empty:
    st.markdown("## 📈 Key Metrics")

    # Create a row of metrics
    cols = st.columns(4)

    # 1. Latest Max Temperature
    with cols[0]:
        latest_max_temp = df['Max Temperature (°C)'].iloc[-1]
        st.metric(
            "Current Max Temperature",
            f"{latest_max_temp:.1f}°C",
            f"{latest_max_temp - df['Max Temperature (°C)'].iloc[-2]:.1f}°C" if len(df) > 1 else None
        )

    # 2. Particulate Matter
    with cols[1]:
        latest_pm = df['PM2_5_CU'].iloc[-1]
        st.metric(
            "Current PM2.5",
            f"{latest_pm:.1f}",
            f"{latest_pm - df['PM2_5_CU'].iloc[-2]:.1f}" if len(df) > 1 else None
        )

    # 3. Mean Color
    with cols[2]:
        latest_color_mean = (df['Mean_Red'].iloc[-1] + df['Mean_Green'].iloc[-1] + df['Mean_Blue'].iloc[-1]) / 3
        st.metric(
            "Average RGB Value",
            f"{latest_color_mean:.1f}",
            f"{latest_color_mean - (df['Mean_Red'].iloc[-2] + df['Mean_Green'].iloc[-2] + df['Mean_Blue'].iloc[-2]) / 3:.1f}" if len(
                df) > 1 else None
        )

    # 4. Particles
    with cols[3]:
        latest_particles = df['particles_beyond_0_3'].iloc[-1]
        st.metric(
            "Particles > 0.3μm",
            f"{latest_particles:.1f}",
            f"{latest_particles - df['particles_beyond_0_3'].iloc[-2]:.1f}" if len(df) > 1 else None
        )

    # MAIN CHARTS SECTION
    st.markdown('<div class="section-header">## 📊 Time Series Analysis</div>', unsafe_allow_html=True)

    # For each category of metrics that has selections
    for category, metrics in selected_metrics.items():
        if metrics:  # If user selected metrics for this category
            st.markdown(f"### {category}")

            # Create a line chart for time series
            fig = go.Figure()

            for metric in metrics:
                fig.add_trace(go.Scatter(
                    x=df['Sequence'],
                    y=df[metric],
                    mode='lines+markers',
                    name=metric
                ))

            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="Sequence",
                yaxis_title="Value",
                hovermode="x unified"
            )

            st.plotly_chart(fig, use_container_width=True)

    # CORRELATION HEATMAP
    st.markdown("### 🔄 Correlation Analysis")

    # Flatten the selected metrics
    all_selected_metrics = []
    for metrics in selected_metrics.values():
        all_selected_metrics.extend(metrics)

    # If we have at least 2 metrics selected
    if len(all_selected_metrics) >= 2:
        correlation = df[all_selected_metrics].corr()

        fig = px.imshow(
            correlation,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            aspect="auto"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least 2 metrics to view correlation analysis")

    # 3D VISUALIZATION FOR COLOR
    st.markdown("### 🎨 RGB Color Visualization")
    if all(col in df.columns for col in ['Mean_Red', 'Mean_Green', 'Mean_Blue']):
        fig = go.Figure(data=[go.Scatter3d(
            x=df['Mean_Red'],
            y=df['Mean_Green'],
            z=df['Mean_Blue'],
            mode='markers',
            marker=dict(
                size=8,
                color=[f'rgb({r},{g},{b})' for r, g, b in zip(
                    df['Mean_Red'],
                    df['Mean_Green'],
                    df['Mean_Blue']
                )],
                opacity=0.8
            )
        )])

        fig.update_layout(
            scene=dict(
                xaxis_title='Red',
                yaxis_title='Green',
                zaxis_title='Blue'
            ),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("RGB color data not available")

    # DATA DOWNLOAD
    st.markdown("### 📥 Data Export")
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f'coffee_environmental_data_{time.strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv',
    )

    # RAW DATA SECTION
    with st.expander("📋 View Raw Data"):
        st.dataframe(df)

else:
    st.warning("No data available. Please check your connection or enable Demo Mode in the sidebar.")

# Footer
st.markdown("---")
st.markdown(f"🕒 **Last updated:** {time.strftime('%Y-%m-%d %H:%M:%S')} | Data points: {len(df)}")
st.markdown("Developed with ❤️ for Coffee Environmental Monitoring")