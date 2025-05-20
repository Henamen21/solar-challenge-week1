# app/utils.py
import pandas as pd
import plotly.express as px
from scipy.stats import f_oneway, kruskal

def dropna_column(dfs, column):
    return [df[column].dropna() for df in dfs]

def run_anova(*args):
    return f_oneway(*args)

def run_kruskal(*args):
    return kruskal(*args)

def plot_boxplot(data, x, y, color):
    fig = px.box(data, x=x, y=y, color=color, title=f"Boxplot of {y} by {x}")
    return fig

def load_and_merge_data(file_paths, country_names):
    """
    Loads multiple CSV files and merges them into one DataFrame.
    Adds a 'Country' column to distinguish data sources.

    Parameters:
    - file_paths: List of file paths to CSVs.
    - country_names: List of country names corresponding to each file.

    Returns:
    - Merged DataFrame with a 'Country' column.
    """
    if len(file_paths) != len(country_names):
        raise ValueError("Number of file paths and country names must match.")

    dataframes = []
    for path, country in zip(file_paths, country_names):
        try:
            df = pd.read_csv(path)
            df["Country"] = country
            dataframes.append(df)
        except Exception as e:
            raise ValueError(f"Failed to load {path}: {e}")

    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df
