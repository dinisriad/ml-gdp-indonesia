"""
=======================================================
  Pengumpulan Data World Bank — Proyek ML GDP Indonesia
  Anggota 2: Mochamad Firmansyah
=======================================================
Cara pakai:
  pip install requests pandas
  python 01_data_collection.py
"""

import requests
import pandas as pd
import os
import time

# ─────────────────────────────────────────
# KONFIGURASI
# ─────────────────────────────────────────
COUNTRY     = "IDN"          # Kode negara Indonesia
START_YEAR  = 1991
END_YEAR    = 2024

INDICATORS = {
    "NY.GDP.MKTP.KD.ZG" : "GDP_Growth",
    "FP.CPI.TOTL.ZG"    : "Inflation",
    "SL.UEM.TOTL.ZS"    : "Unemployment",
    "SP.POP.GROW"        : "Population_Growth",
    "NE.EXP.GNFS.ZS"    : "Exports",
    "NE.IMP.GNFS.ZS"    : "Imports",
    "BX.KLT.DINV.WD.GD.ZS": "FDI",
    "PA.NUS.FCRF"        : "Exchange_Rate",
}

RAW_DIR       = "data/raw"
PROCESSED_DIR = "data/processed"

# ─────────────────────────────────────────
# FUNGSI UTAMA
# ─────────────────────────────────────────

def fetch_indicator(indicator_code, col_name):
    """Ambil satu indikator dari World Bank API."""
    url = (
        f"https://api.worldbank.org/v2/country/{COUNTRY}"
        f"/indicator/{indicator_code}"
        f"?date={START_YEAR}:{END_YEAR}"
        f"&format=json&per_page=100"
    )

    print(f"  → Mengambil {col_name} ({indicator_code}) ...", end=" ")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # World Bank mengembalikan list 2 elemen: [metadata, data]
        records = data[1]
        rows = []
        for record in records:
            year  = int(record["date"])
            value = record["value"]   # bisa None kalau data kosong
            rows.append({"Year": year, col_name: value})

        df = pd.DataFrame(rows).sort_values("Year").reset_index(drop=True)
        print(f"✅  ({len(df)} baris)")
        return df

    except requests.exceptions.RequestException as e:
        print(f"❌  Error: {e}")
        return None


def validate_dataset(df):
    """Validasi kualitas dataset gabungan."""
    print("\n" + "="*50)
    print("VALIDASI DATASET")
    print("="*50)

    # 1. Bentuk data
    print(f"\n📐 Shape       : {df.shape[0]} baris x {df.shape[1]} kolom")
    print(f"📅 Rentang Tahun: {df['Year'].min()} — {df['Year'].max()}")

    # 2. Missing values
    print("\n🔍 Missing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    summary = pd.DataFrame({
        "Missing": missing,
        "Persen (%)": missing_pct
    })
    print(summary.to_string())

    # 3. Duplikasi
    duplikat = df.duplicated(subset="Year").sum()
    print(f"\n🔁 Duplikasi tahun: {duplikat}")

    # 4. Statistik deskriptif
    print("\n📊 Statistik Deskriptif:")
    print(df.describe().round(3).to_string())

    return summary


def save_data_quality_report(df, missing_summary):
    """Simpan laporan kualitas data ke docs/."""
    os.makedirs("docs", exist_ok=True)

    lines = []
    lines.append("# Data Quality Report\n")
    lines.append(f"**Periode:** {df['Year'].min()} — {df['Year'].max()}\n")
    lines.append(f"**Jumlah baris:** {len(df)}\n")
    lines.append(f"**Jumlah kolom:** {len(df.columns)}\n\n")

    lines.append("## Missing Values\n")
    lines.append("| Variabel | Missing | Persen (%) |\n")
    lines.append("|---|---|---|\n")
    for col in missing_summary.index:
        if col == "Year":
            continue
        m   = missing_summary.loc[col, "Missing"]
        pct = missing_summary.loc[col, "Persen (%)"]
        lines.append(f"| {col} | {m} | {pct}% |\n")

    lines.append("\n## Catatan Outlier\n")
    lines.append("- **1998**: Krisis moneter Asia — GDP Growth turun drastis (~-13%)\n")
    lines.append("- **2020**: Pandemi COVID-19 — kontraksi ekonomi global (~-2%)\n")
    lines.append("- Kedua outlier ini **valid secara historis**, jangan dihapus.\n")

    lines.append("\n## Kesimpulan\n")
    lines.append("Dataset cukup bersih. Missing values minor dan dapat dihandle dengan interpolasi linear.\n")

    with open("docs/data_quality_report.md", "w") as f:
        f.writelines(lines)

    print("\n📄 Laporan disimpan → docs/data_quality_report.md")


def save_data_dictionary():
    """Simpan kamus data ke docs/."""
    os.makedirs("docs", exist_ok=True)

    rows = [
        ("GDP_Growth",        "%",        "NY.GDP.MKTP.KD.ZG",     "Target prediksi — pertumbuhan GDP per tahun"),
        ("Inflation",         "%",        "FP.CPI.TOTL.ZG",        "Tingkat inflasi tahunan berdasarkan CPI"),
        ("Unemployment",      "%",        "SL.UEM.TOTL.ZS",        "Tingkat pengangguran dari total angkatan kerja"),
        ("Population_Growth", "%",        "SP.POP.GROW",           "Pertumbuhan populasi tahunan"),
        ("Exports",           "% GDP",    "NE.EXP.GNFS.ZS",        "Nilai ekspor barang dan jasa"),
        ("Imports",           "% GDP",    "NE.IMP.GNFS.ZS",        "Nilai impor barang dan jasa"),
        ("FDI",               "% GDP",    "BX.KLT.DINV.WD.GD.ZS", "Foreign Direct Investment neto"),
        ("Exchange_Rate",     "IDR/USD",  "PA.NUS.FCRF",           "Nilai tukar resmi Rupiah terhadap USD"),
    ]

    lines = []
    lines.append("# Data Dictionary\n\n")
    lines.append("| Variabel | Satuan | Kode World Bank | Keterangan |\n")
    lines.append("|---|---|---|---|\n")
    for nama, satuan, kode, ket in rows:
        lines.append(f"| {nama} | {satuan} | `{kode}` | {ket} |\n")

    lines.append(f"\n**Sumber:** World Bank Open Data (https://data.worldbank.org)\n")
    lines.append(f"**Negara:** Indonesia (IDN)\n")
    lines.append(f"**Rentang tahun:** {START_YEAR}–{END_YEAR}\n")

    with open("docs/data_dictionary.md", "w") as f:
        f.writelines(lines)

    print("📄 Kamus data disimpan → docs/data_dictionary.md")


# ─────────────────────────────────────────
# JALANKAN
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Buat folder
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    print("="*50)
    print("  PENGUMPULAN DATA WORLD BANK")
    print(f"  Negara: Indonesia | {START_YEAR}–{END_YEAR}")
    print("="*50 + "\n")

    # 1. Ambil semua indikator satu per satu
    dataframes = []
    for kode, nama in INDICATORS.items():
        df_ind = fetch_indicator(kode, nama)
        if df_ind is not None:
            # Simpan CSV mentah
            path_raw = os.path.join(RAW_DIR, f"{nama.lower()}.csv")
            df_ind.to_csv(path_raw, index=False)
            dataframes.append(df_ind)
        time.sleep(0.3)   # jeda kecil agar tidak rate-limit

    # 2. Gabungkan semua indikator berdasarkan Year
    print("\n🔗 Menggabungkan semua indikator ...")
    df_all = dataframes[0]
    for df_next in dataframes[1:]:
        df_all = pd.merge(df_all, df_next, on="Year", how="outer")

    df_all = df_all.sort_values("Year").reset_index(drop=True)

    # Urutkan kolom
    cols_order = ["Year", "GDP_Growth", "Inflation", "Unemployment",
                  "Population_Growth", "Exports", "Imports", "FDI", "Exchange_Rate"]
    df_all = df_all[cols_order]

    # 3. Simpan dataset final
    output_path = os.path.join(PROCESSED_DIR, "dataset_indonesia.csv")
    df_all.to_csv(output_path, index=False)
    print(f"💾 Dataset disimpan → {output_path}")

    # 4. Validasi
    missing_summary = validate_dataset(df_all)

    # 5. Hitung korelasi awal
    print("\n📈 Korelasi dengan GDP_Growth:")
    corr = df_all.drop("Year", axis=1).corr()["GDP_Growth"].sort_values(ascending=False)
    print(corr.round(3).to_string())
    corr_path = os.path.join(PROCESSED_DIR, "correlation_matrix.csv")
    df_all.drop("Year", axis=1).corr().to_csv(corr_path)
    print(f"\n💾 Matriks korelasi disimpan → {corr_path}")

    # 6. Simpan dokumentasi
    save_data_quality_report(df_all, missing_summary)
    save_data_dictionary()

    print("\n" + "="*50)
    print("✅  SELESAI! Semua file berhasil dibuat.")
    print("="*50)
    print("\nFile yang dihasilkan:")
    print(f"  📁 {RAW_DIR}/               ← 8 file CSV mentah per indikator")
    print(f"  📄 {output_path}  ← Dataset final gabungan")
    print(f"  📄 data/processed/correlation_matrix.csv")
    print(f"  📄 docs/data_quality_report.md")
    print(f"  📄 docs/data_dictionary.md")
