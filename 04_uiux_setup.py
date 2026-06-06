"""
=======================================================
  Setup Aset UI/UX — Proyek ML GDP Indonesia
  Anggota 4: Nazwa Nur Hapidah (UI/UX Designer)
=======================================================
"""
import os

print("="*50)
print("✨ NAZWA (UI/UX) - MEMBUAT ASET DESAIN UNTUK RAUFAN")
print("="*50)

# 1. Buat struktur folder assets dan docs jika belum ada
os.makedirs('assets', exist_ok=True)
os.makedirs('docs/wireframe', exist_ok=True)

# 2. Generate CSS Kustom yang dicari oleh app.py-nya Raufan
print("💅 Menulis file assets/style.css...")
with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write("""/* =========================================
   STYLE CSS CUSTOM - OLEH NAZWA (UI/UX)
   ========================================= */

/* Kustomisasi warna tombol utama Streamlit */
.stButton > button {
    background-color: #1D6FA4 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: bold !important;
}

/* Kustomisasi Judul Utama agar berwarna Biru Profesional */
h1 {
    color: #1D6FA4 !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}

/* Kustomisasi Card Metrik (Angka Prediksi) */
[data-testid="metric-container"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E0E4E8 !important;
    border-left: 5px solid #1D6FA4 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}
""")

# 3. Generate Design Guide untuk dokumentasi proyek
print("📝 Menulis file docs/design_guide.md...")
with open('docs/design_guide.md', 'w', encoding='utf-8') as f:
    f.write("""# 🎨 Design Guide — GDP Prediction App

## 1. Color Palette
- **Primary:** `#1D6FA4` (Biru Profesional)
- **Background:** `#F8F9FA`
- **Text:** `#212529`

## 2. Typography
- menggunakan font standar modern bawaan Streamlit dengan penekanan Bold pada Header.
""")

print("\n✅ SELESAI! File 'assets/style.css' sudah siap. Sekarang app.py tidak akan error lagi!")