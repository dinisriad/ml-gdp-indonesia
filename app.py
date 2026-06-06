import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.title("Tren Historis & Proyeksi Interaktif")
st.markdown("Grafik di bawah memadukan **data nyata sejak 1991** dengan **proyeksi Machine Learning untuk 5 tahun ke depan (2025–2029)**. Garis oranye/hitam = realita. Garis biru = prediksi.")

# Pastikan file data historis dan data proyeksi buatan Fauzi sudah ada
if os.path.exists('data/processed/dataset_indonesia.csv') and os.path.exists('data/processed/proyeksi_gdp.csv'):
    
    df_hist = pd.read_csv('data/processed/dataset_indonesia.csv')
    df_proj = pd.read_csv('data/processed/proyeksi_gdp.csv')

    # Titik sambung (Ambil data tahun terakhir, yaitu 2024)
    last_hist_year = df_hist['Year'].iloc[-1]
    last_hist_gdp = df_hist['GDP_Growth'].iloc[-1]

    # Gabungkan titik 2024 dengan prediksi 2025-2029 agar garisnya menyambung tanpa putus
    future_years = [last_hist_year] + df_proj['Year'].tolist()
    predicted_gdp = [last_hist_gdp] + df_proj['Predicted_GDP'].tolist()
    upper_bound = [last_hist_gdp] + df_proj['Upper_Bound'].tolist()
    lower_bound = [last_hist_gdp] + df_proj['Lower_Bound'].tolist()

    # ==========================================
    # MEMBUAT GRAFIK INTERAKTIF MENGGUNAKAN PLOTLY
    # ==========================================
    fig = go.Figure()

    # 1. Plot Pita Biru Muda (Rentang Toleransi Error / Confidence Interval)
    fig.add_trace(go.Scatter(
        x=future_years + future_years[::-1],
        y=upper_bound + lower_bound[::-1],
        fill='toself',
        fillcolor='rgba(135, 206, 250, 0.3)', # Biru muda transparan
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Rentang Toleransi Error'
    ))

    # 2. Plot Garis Historis dari Firmansyah (Oranye/Hitam)
    fig.add_trace(go.Scatter(
        x=df_hist['Year'], 
        y=df_hist['GDP_Growth'],
        mode='lines+markers',
        name='Data Historis (Realita)',
        line=dict(color='black', width=1),
        marker=dict(color='orange', size=6, line=dict(color='white', width=1))
    ))

    # 3. Plot Garis Prediksi Masa Depan dari Fauzi (Biru)
    fig.add_trace(go.Scatter(
        x=future_years, 
        y=predicted_gdp,
        mode='lines',
        name='Proyeksi Masa Depan (AI)',
        line=dict(color='#1D6FA4', width=3)
    ))

    # 4. Tambahkan Teks Anotasi Krisis
    fig.add_annotation(x=1998, y=-13.1, text="Krisis Asia '98", showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color="red", size=10))
    fig.add_annotation(x=2020, y=-2.07, text="Pandemi COVID-19", showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color="red", size=10))

    # 5. Percantik Tampilan
    fig.update_layout(
        title=dict(text="Lintasan Pertumbuhan Ekonomi Indonesia | Data Historis vs Proyeksi AI", font=dict(size=18, color='black')),
        xaxis=dict(title='Tahun', showgrid=True, gridcolor='lightgray'),
        yaxis=dict(title='Pertumbuhan GDP (%)', showgrid=True, gridcolor='lightgray', zeroline=True, zerolinecolor='gray'),
        plot_bgcolor='white',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Tampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Tips:** Hover kursor ke grafik untuk melihat nilai persis tiap tahun. Area biru muda = Rentang toleransi error prediksi AI.")
else:
    st.error("⚠️ Data historis atau data proyeksi belum tersedia. Pastikan script Fauzi sudah dijalankan!")