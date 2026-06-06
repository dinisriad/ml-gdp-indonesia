import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_gdp_trend(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df['Year'], df['GDP_Growth'], marker='o', color='steelblue')
    ax.axhline(0, color='red', linestyle='--', alpha=0.5)
    ax.set_title('Tren GDP Growth Indonesia')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('GDP Growth (%)')
    ax.grid(True, alpha=0.3)
    return fig

def plot_heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df.drop('Year', axis=1).corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Heatmap Korelasi')
    return fig
