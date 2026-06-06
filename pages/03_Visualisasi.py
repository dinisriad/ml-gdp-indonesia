import streamlit as st
import pandas as pd
import sys
sys.path.append('.')
from scripts.visualization import plot_gdp_trend, plot_heatmap, plot_scatter

st.title("📊 Visualisasi Data")
st.markdown("---")

df = pd.read_csv('data/processed/dataset_indonesia.csv')

st.subheader("Tren GDP Growth Indonesia (1991-2024)")
fig = plot_gdp_trend(df)
st.pyplot(fig)

st.subheader("Heatmap Korelasi")
fig2 = plot_heatmap(df)
st.pyplot(fig2)

st.subheader("Hubungan GDP Growth dengan Variabel Lain")
feature = st.selectbox("Pilih variabel:",
    ['Inflation','Unemployment','Population_Growth','Exports','Imports','FDI','Exchange_Rate'])
fig3 = plot_scatter(df, feature)
st.pyplot(fig3)