import streamlit as st
import sys
sys.path.append('.')
from utils.predictor import load_model, preprocess_input, predict

st.title("🔮 Prediksi GDP Growth")
st.markdown("---")

with st.expander("ℹ️ Penjelasan Variabel"):
    st.markdown("""
    - **Inflation**: Tingkat inflasi (%)
    - **Unemployment**: Tingkat pengangguran (%)
    - **Population Growth**: Pertumbuhan populasi (%)
    - **Exports**: Nilai ekspor sebagai % GDP
    - **Imports**: Nilai impor sebagai % GDP
    - **FDI**: Investasi asing langsung (% GDP)
    - **Exchange Rate**: Kurs IDR terhadap USD
    """)

st.subheader("Masukkan Nilai Indikator")
col1, col2 = st.columns(2)

with col1:
    inflation = st.number_input("Inflation (%)", value=3.5)
    unemployment = st.number_input("Unemployment (%)", value=5.0)
    pop_growth = st.number_input("Population Growth (%)", value=1.1)
    exports = st.number_input("Exports (% GDP)", value=20.0)

with col2:
    imports = st.number_input("Imports (% GDP)", value=18.0)
    fdi = st.number_input("FDI (% GDP)", value=2.5)
    exchange_rate = st.number_input("Exchange Rate (IDR/USD)", value=15000.0)

if st.button("🚀 Prediksi Sekarang"):
    model, scaler, report = load_model()
    input_data = [inflation, unemployment, pop_growth, exports, imports, fdi, exchange_rate]
    result = predict(model, scaler, input_data)

    st.success(f"### Prediksi GDP Growth: **{result:.2f}%**")

    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{report['MAE']:.4f}")
    col2.metric("RMSE", f"{report['RMSE']:.4f}")
    col3.metric("R² Score", f"{report['R2']:.4f}")