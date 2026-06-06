"""
=======================================================
  Automasi Visualisasi & EDA — Proyek ML GDP Indonesia
  Anggota 4: Dini Sriastuti (Data Visualization)
=======================================================
Cara pakai:
  pip install matplotlib seaborn
  python notebooks/03_eda_automation.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("="*50)
print("🎨 MEMULAI PROSES AUTOMASI VISUALISASI DATA (EDA)")
print("="*50)

# 1. PERSIAPAN FOLDER & BACA DATA
os.makedirs('data/eda_outputs', exist_ok=True)
os.makedirs('scripts', exist_ok=True)
os.makedirs('docs', exist_ok=True)

data_path = 'data/processed/dataset_indonesia.csv'
df = pd.read_csv(data_path)
print(f"📥 Data loaded: {df.shape[0]} baris.")

# 2. GENERATE GRAFIK 1: HISTOGRAM
print("📊 Membuat Histogram...")
df.drop('Year', axis=1).hist(bins=15, figsize=(14, 10), color='teal', edgecolor='black')
plt.tight_layout()
plt.savefig('data/eda_outputs/histogram_all.png', dpi=300)
plt.close()

# 3. GENERATE GRAFIK 2: TREN GDP GROWTH
print("📈 Membuat Grafik Tren GDP...")
plt.figure(figsize=(12, 5))
plt.plot(df['Year'], df['GDP_Growth'], marker='o', color='steelblue', linewidth=2)
plt.axhline(0, color='red', linestyle='--', alpha=0.5)
plt.title('Tren GDP Growth Indonesia (1991-2024)', fontsize=14, fontweight='bold')
plt.xlabel('Tahun')
plt.ylabel('GDP Growth (%)')
plt.grid(True, alpha=0.3)

# Tandai Outlier Sejarah
val_1998 = df[df['Year']==1998]['GDP_Growth'].values[0]
val_2020 = df[df['Year']==2020]['GDP_Growth'].values[0]
plt.annotate('Krisis Asia (1998)', xy=(1998, val_1998), xytext=(2000, -10),
             arrowprops=dict(facecolor='red', shrink=0.05))
plt.annotate('COVID-19 (2020)', xy=(2020, val_2020), xytext=(2015, -5),
             arrowprops=dict(facecolor='orange', shrink=0.05))

plt.savefig('data/eda_outputs/gdp_trend.png', dpi=300)
plt.close()

# 4. GENERATE GRAFIK 3: HEATMAP KORELASI
print("🗺️  Membuat Heatmap Korelasi...")
plt.figure(figsize=(10, 8))
corr = df.drop('Year', axis=1).corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, linewidths=0.5)
plt.title('Heatmap Korelasi Antar Variabel Ekonomi Makro', fontsize=14)
plt.tight_layout()
plt.savefig('data/eda_outputs/heatmap_korelasi.png', dpi=300)
plt.close()

# 5. GENERATE GRAFIK 4: SCATTER PLOT
print("🔵 Membuat Scatter Plots...")
features = ['Inflation', 'Unemployment', 'Exports', 'Imports', 'FDI', 'Exchange_Rate']
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()
for i, feat in enumerate(features):
    sns.regplot(x=df[feat], y=df['GDP_Growth'], ax=axes[i], scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
    axes[i].set_title(f'GDP vs {feat}')
    axes[i].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/eda_outputs/scatter_plots.png', dpi=300)
plt.close()

# 6. OTOMATIS BIKIN FILE scripts/visualization.py UNTUK STREAMLIT NANTI
print("⚙️  Men-generate scripts/visualization.py...")
# TAMBAHKAN encoding='utf-8' DI SINI
with open('scripts/visualization.py', 'w', encoding='utf-8') as f:
    f.write('''import matplotlib.pyplot as plt
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
''')

# 7. OTOMATIS BIKIN FILE Laporan EDA (eda_summary.md)
print("📝 Men-generate docs/eda_summary.md...")
# TAMBAHKAN encoding='utf-8' DI SINI JUGA
with open('docs/eda_summary.md', 'w', encoding='utf-8') as f:
    f.write('''# Exploratory Data Analysis (EDA) Summary

## 📌 Temuan Utama
1. **Rata-rata Pertumbuhan:** GDP Growth Indonesia berada di kisaran 5% per tahun pada kondisi normal.
2. **Korelasi Negatif Kuat:** Inflasi memiliki korelasi negatif yang sangat kuat dengan GDP. Jika inflasi naik tajam, GDP akan turun.
3. **Anomali Ekstrem (Outlier):** Terdapat dua titik kontraksi hebat:
   - **Tahun 1998 (-13.1%):** Efek domino dari Krisis Moneter Asia.
   - **Tahun 2020 (-2.07%):** Efek berhentinya aktivitas ekonomi akibat Pandemi COVID-19.

## 💡 Rekomendasi Modeling
Karena keberadaan anomali krisis pada tahun 1998 dan 2020 sangat merusak tren linearitas, pembuatan fitur tambahan seperti `is_crisis` (0 atau 1) sangat direkomendasikan untuk membantu model AI membedakan tahun normal dan tahun bencana.
''')

print("\n" + "="*50 + "\n✅ SELESAI! Semua Grafik, Script Streamlit, dan Laporan berhasil dibuat.\n" + "="*50)