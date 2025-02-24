import pandas as pd
import numpy as np

def load_data(num_points=100):
    df = pd.DataFrame({
        "x": np.linspace(0, 10, num_points),
        "y": np.sin(np.linspace(0, 10, num_points)) + np.random.normal(scale=0.2, size=num_points)
    })
    return df
