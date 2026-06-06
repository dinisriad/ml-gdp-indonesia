import streamlit as st

st.set_page_config(
    page_title="Prediksi GDP Indonesia",
    page_icon="📈",
    layout="wide"
)

# Load CSS custom (dari Nazwa)
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.title("📊 GDP Prediction")
st.sidebar.markdown("Navigasi menggunakan menu di atas")