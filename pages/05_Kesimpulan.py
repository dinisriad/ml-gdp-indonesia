import streamlit as st
import pandas as pd
import json

st.title("📝 Kesimpulan")
st.markdown("---")

with open('models/model_report.json') as f:
    report = json.load(f)

st.subheader("Perbandingan Model")
df_report = pd.DataFrame(report).T
st.dataframe(df_report, use_container_width=True)

st.subheader("Temuan EDA")
with open('docs/eda_summary.md') as f:
    st.markdown(f.read())