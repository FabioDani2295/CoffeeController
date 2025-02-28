import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Any


# Data processing functions
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data for better visualization
    """
    # Create a copy to avoid modifying the original
    processed_df = df.copy()

    # Handle missing values if any
    processed_df = processed_df.fillna(0)

    # Add timestamp if it doesn't exist (for demo purposes)
    if 'timestamp' not in processed_df.columns:
        processed_df['timestamp'] = pd.date_range(
            start=pd.Timestamp.now() - pd.Timedelta(days=len(processed_df) - 1),
            periods=len(processed_df),
            freq='D'
        )

    return processed_df


def get_temperature_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate temperature statistics
    """
    temp_cols = [col for col in df.columns if 'Temperature' in col]
    if not temp_cols:
        return {}

    summary = {
        'max_temperature': df['Max Temperature (°C)'].max(),
        'min_temperature': df['Min Temperature (°C)'].min(),
        'avg_temperature': df['Mean Temperature (°C)'].mean(),
        'temperature_range': df['Max Temperature (°C)'].max() - df['Min Temperature (°C)'].min(),
        'above_40_percent': df['% Pixels Above 40°C'].mean()
    }

    return summary


def get_pm_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate particulate matter statistics
    """
    pm_cols = [col for col in df.columns if col.startswith('PM')]
    if not pm_cols:
        return {}

    summary = {col: df[col].mean() for col in pm_cols}
    summary['max_pm'] = max([df[col].max() for col in pm_cols])

    return summary


def get_color_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate color statistics
    """
    color_cols = ['Mean_Red', 'Mean_Green', 'Mean_Blue']
    if not all(col in df.columns for col in color_cols):
        return {}

    summary = {
        'avg_red': df['Mean_Red'].mean(),
        'avg_green': df['Mean_Green'].mean(),
        'avg_blue': df['Mean_Blue'].mean(),
        'color_variance': np.var([df['Mean_Red'].mean(), df['Mean_Green'].mean(), df['Mean_Blue'].mean()])
    }

    return summary


# Visualization functions
def create_multi_y_axis_chart(df: pd.DataFrame, primary_cols: List[str], secondary_cols: List[str], title: str):
    """
    Create a chart with multiple y-axes
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for primary y-axis
    for col in primary_cols:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[col], name=col),
            secondary_y=False,
        )

    # Add traces for secondary y-axis
    for col in secondary_cols:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[col], name=col, line=dict(dash='dot')),
            secondary_y=True,
        )

    # Add figure title
    fig.update_layout(
        title_text=title,
        height=500
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Measurement Sequence")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Primary</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Secondary</b>", secondary_y=True)

    return fig


def create_color_visualization(df: pd.DataFrame):
    """
    Create a color visualization from RGB values
    """
    if not all(col in df.columns for col in ['Mean_Red', 'Mean_Green', 'Mean_Blue']):
        return None

    # Create the color swatches
    fig, ax = plt.subplots(1, len(df), figsize=(len(df) * 0.5, 1))

    # If there's only one datapoint, we need to handle differently
    if len(df) == 1:
        r, g, b = df['Mean_Red'].iloc[0] / 255, df['Mean_Green'].iloc[0] / 255, df['Mean_Blue'].iloc[0] / 255
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=(r, g, b)))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
    else:
        for i in range(len(df)):
            r, g, b = df['Mean_Red'].iloc[i] / 255, df['Mean_Green'].iloc[i] / 255, df['Mean_Blue'].iloc[i] / 255
            ax[i].add_patch(plt.Rectangle((0, 0), 1, 1, color=(r, g, b)))
            ax[i].set_xticks([])
            ax[i].set_yticks([])
            ax[i].set_frame_on(False)

    # Convert the figure to a base64 image
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close(fig)

    return f'data:image/png;base64,{img_str}'