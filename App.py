import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="☕ Coffee Assessment Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for a more compact design
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

    /* High contrast metrics styling */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 0.5rem;
        border-radius: 0.3rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    [data-testid="stMetric"] > div {
        font-size: 0.9rem !important;
        color: #333 !important;
        font-weight: bold;
    }
    [data-testid="stMetric"] > div:nth-child(2) {
        font-size: 1.2rem !important;
        color: #000 !important;
    }
    [data-testid="stMetricDelta"] {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 2px 5px;
        border-radius: 3px;
        color: #333 !important;
    }
    [data-testid="stMetricDelta"] svg {
        display: none !important;
    }
    .stPlotlyChart {
        height: auto !important;
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
    /* Slim down metric tiles and make text black */
    [data-testid="stMetric"] {
        background-color: #f9f9f9;
        padding: 0.5rem;
        border-radius: 0.3rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        color: black !important;
    }
    [data-testid="stMetric"] > div {
        font-size: 0.9rem !important;
        color: black !important;
    }
    [data-testid="stMetric"] > div:nth-child(2) {
        font-size: 1.2rem !important;
        color: black !important;
    }
    /* Make metric delta label black */
    [data-testid="stMetricDelta"] {
        color: black !important;
    }
    [data-testid="stMetricDelta"] > div {
        color: black !important;
    }
    /* Ensure all text in the metrics section is black */
    .metric-container * {
        color: black !important;
    }
    /* Dataframe styling */
    .dataframe-container {
        font-size: 0.8rem;
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
        # Add a Sample ID column for tracking
        df['Sample ID'] = range(1, len(df) + 1)
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

# SIDEBAR - Make it more compact
with st.sidebar:
    st.markdown("### ⚙️ Dashboard Controls")

    # Refresh rate control
    st.slider(
        "Refresh Rate (sec)",
        min_value=5,
        max_value=120,
        value=st.session_state.refresh_rate,
        step=5,
        key="refresh_rate_input",
        on_change=lambda: setattr(st.session_state, 'refresh_rate', st.session_state.refresh_rate_input)
    )

    # Demo mode toggle
    st.checkbox(
        "Demo Mode",
        value=st.session_state.demo_mode,
        key="demo_mode_input",
        on_change=lambda: setattr(st.session_state, 'demo_mode', st.session_state.demo_mode_input),
        help="Use local data if online source unavailable"
    )

    # Organize columns by category
    column_categories = {
        "Temperature": [col for col in df.columns if "Temperature" in col],
        "Particulate Matter": [col for col in df.columns if "PM" in col],
        "Particles": [col for col in df.columns if "particles_beyond" in col],
        "Color": ['Mean_Red', 'Mean_Green', 'Mean_Blue', 'L*', 'a*', 'b*', 'Dist_White', 'Dist_Gray'],
        "Values": ['Min Value', 'Max Value', 'Range', 'Mean']
    }

    # Sidebar metric selection
    st.markdown("### 📊 Metrics")
    selected_metrics = {}

    # For each category, create a multiselect with smaller height
    for category, columns in column_categories.items():
        if columns:  # Only show categories with columns
            default_selection = st.session_state.selected_metrics.get(category, columns[:2])
            selected_metrics[category] = st.multiselect(
                f"{category}",
                options=columns,
                default=default_selection,
                key=f"select_{category}"
            )
            # Update session state
            st.session_state.selected_metrics[category] = selected_metrics[category]

# MAIN DASHBOARD
st.markdown('<div class="main-header">☕ Coffee Assessment Analysis</div>', unsafe_allow_html=True)

# LATEST COFFEE SAMPLE COMPARISON
if not df.empty:
    # Get the latest coffee sample (last row) and previous samples
    latest_sample = df.iloc[-1]

    st.markdown('<div class="section-header">Latest Coffee Sample Assessment</div>', unsafe_allow_html=True)

    # Create two columns - latest coffee metrics and comparison
    col1, col2 = st.columns([1, 2])

    # Create one column for the latest coffee metrics
    st.markdown(
        '<h4 style="color: white; background-color: #333; padding: 5px; border-radius: 5px;">Sample #{}</h4>'.format(
            len(df)), unsafe_allow_html=True)

    # Compact metrics display for latest sample in a single row
    key_metrics = [
        ("Max Temp", "Max Temperature (°C)", "°C"),
        ("Mean Temp", "Mean Temperature (°C)", "°C"),
        ("PM2.5", "PM2_5_CU", ""),
        ("Particles >0.3μm", "particles_beyond_0_3", "")
    ]

    # Create a row of metrics
    metric_cols = st.columns(len(key_metrics))

    for i, (label, col_name, unit) in enumerate(key_metrics):
        if col_name in df.columns:
            with metric_cols[i]:
                value = latest_sample[col_name]
                # Calculate comparison with average of all previous samples
                if len(df) > 1:
                    avg_prev = df.iloc[:-1][col_name].mean()
                    diff = value - avg_prev
                    st.metric(
                        label,
                        f"{value:.1f}{unit}",
                        f"{diff:+.1f}{unit} vs avg",
                        delta_color="normal"
                    )
                else:
                    st.metric(label, f"{value:.1f}{unit}")

    # Create two columns for the image and color display
    img_col, color_col = st.columns([3, 1])

    with col1:
        # Add RGB color display if available
        if all(col in df.columns for col in ['Mean_Red', 'Mean_Green', 'Mean_Blue']):
            r, g, b = int(latest_sample['Mean_Red']), int(latest_sample['Mean_Green']), int(latest_sample['Mean_Blue'])
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

        # Display coffee image if available
        try:
            st.image("ImageData.jpg", caption="Latest Coffee Sample Image", use_container_width=True)
        except Exception as e:
            st.warning(f"Coffee image not available: {e}")

with col2:
    # Create radar chart comparing latest to average of previous samples
    if len(df) > 1:
        # Select metrics for radar chart with exact columns as specified
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

        # Filter to metrics that exist in the dataframe
        radar_metrics = [m for m in radar_metrics if m in df.columns]

        if radar_metrics:
            # Calculate the average of previous samples
            avg_previous = df.iloc[:-1][radar_metrics].mean()

            # Normalize the data for better visualization
            max_values = df[radar_metrics].max()
            min_values = df[radar_metrics].min()

            # Avoid division by zero
            range_values = max_values - min_values
            range_values = range_values.replace(0, 1)  # Replace zeros with 1 to avoid division by zero

            # Normalize latest and average values
            latest_normalized = (latest_sample[radar_metrics] - min_values) / range_values
            avg_normalized = (avg_previous - min_values) / range_values

            # Create radar chart
            fig = go.Figure()

            # Add trace for average previous
            fig.add_trace(go.Scatterpolar(
                r=avg_normalized.values,
                theta=radar_metrics,
                fill='toself',
                name='Average Previous',
                line=dict(color='rgba(135, 206, 250, 0.7)'),
            ))

            # Add trace for latest sample
            fig.add_trace(go.Scatterpolar(
                r=latest_normalized.values,
                theta=radar_metrics,
                fill='toself',
                name='Latest Sample',
                line=dict(color='rgba(255, 99, 71, 0.8)'),
            ))

            # Update layout
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                margin=dict(l=30, r=30, t=20, b=30),
                height=400,
                font=dict(color="black")
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient metrics available for comparison")
    else:
        st.info("Only one sample available. More samples needed for comparison.")

# HISTORICAL TRENDS
st.markdown('<div class="section-header">Historical Sample Analysis</div>', unsafe_allow_html=True)

# Create tabs for different categories of metrics
tabs = st.tabs([
    "Temperature",
    "Particulate",
    "Color",
    "Particles",
    "Values"
])

# Temperature tab
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

# Particulate tab
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

# Color tab
with tabs[2]:
    color_metrics = selected_metrics.get("Color", [])
    if color_metrics and 'Mean_Red' in df.columns and 'Mean_Green' in df.columns and 'Mean_Blue' in df.columns:
        col1, col2 = st.columns([3, 1])

        with col1:
            # Line chart for selected color metrics
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
            # Color swatches for all samples
            st.markdown("#### Color Swatches")
            for i in range(len(df)):
                r, g, b = int(df.iloc[i]['Mean_Red']), int(df.iloc[i]['Mean_Green']), int(df.iloc[i]['Mean_Blue'])
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

# Particles tab
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

# Values tab
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

# STATISTICAL COMPARISON
st.markdown('<div class="section-header">Statistical Analysis</div>', unsafe_allow_html=True)

# Use full width for correlation matrix
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
        height=500
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10)
    )
    # Make the font more readable
    fig.update_traces(textfont=dict(size=10))

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Select at least 2 metrics to view correlations")

# Create columns for percentile analysis
col1, col2 = st.columns(2)

with col1:
    # Latest sample percentile ranking among all samples
    if len(df) > 1:
        # Select metrics to rank
        rank_metrics = ["Max Temperature (°C)", "PM2_5_CU", "particles_beyond_0_3"]
        rank_metrics = [m for m in rank_metrics if m in df.columns]

        if rank_metrics:
            # Calculate percentile ranks for the latest sample
            percentile_ranks = {}
            for metric in rank_metrics:
                all_values = df[metric].sort_values().values
                latest_value = latest_sample[metric]
                # Find position of the latest value
                percentile = sum(all_values < latest_value) / len(all_values) * 100
                percentile_ranks[metric] = percentile

            # Create bar chart of percentiles
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
    # Display placeholder to avoid empty column
    st.write("")

# RAW DATA VIEW - more compact
with st.expander("View Raw Data"):
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download button
    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f"coffee_assessment_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

else:
st.warning("No data available. Please check your connection or enable Demo Mode in the sidebar.")

# Footer - made more compact with Rome timezone
rome_tz = pytz.timezone('Europe/Rome')
rome_time = datetime.now(rome_tz).strftime('%Y-%m-%d %H:%M:%S')

st.markdown(f"""
<div style="text-align: center; font-size: 0.8rem; margin-top: 1rem; color: #666;">
    Last updated: {rome_time} (Rome Time) | Total Samples: {len(df)}
</div>
""", unsafe_allow_html=True)