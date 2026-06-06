import streamlit as st
import pandas as pd

st.title("📂 Dataset")
st.markdown("---")

df = pd.read_csv('data/processed/dataset_indonesia.csv')

st.subheader("Preview Data")
st.dataframe(df, use_container_width=True)

st.subheader("Statistik Deskriptif")
st.dataframe(df.describe(), use_container_width=True)

st.subheader("Kamus Variabel")
kamus = {
    'Variabel': ['GDP_Growth','Inflation','Unemployment','Population_Growth',
                 'Exports','Imports','FDI','Exchange_Rate'],
    'Keterangan': ['Pertumbuhan GDP (%)','Inflasi (%)','Pengangguran (%)',
                   'Pertumbuhan Populasi (%)','Ekspor (% GDP)','Impor (% GDP)',
                   'Foreign Direct Investment (% GDP)','Kurs (IDR/USD)'],
    'Satuan': ['%','%','%','%','% GDP','% GDP','% GDP','IDR']
}
st.table(pd.DataFrame(kamus))