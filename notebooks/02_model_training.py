"""
=======================================================
  Pelatihan Model ML — Proyek ML GDP Indonesia
  Anggota 3: Fauzi Rizky Maulana (Data Scientist)
=======================================================
Cara pakai:
  python notebooks/02_model_training.py
"""

import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("="*50)
print("🚀 MEMULAI PIPELINE MACHINE LEARNING")
print("="*50)

# 1. BACA DATA
data_path = 'data/processed/dataset_indonesia.csv'
df = pd.read_csv(data_path)
print(f"📥 Data loaded: {df.shape[0]} baris.")

# 2. PREPROCESSING (Handle Missing & Outlier)
# Set index tahun dan interpolasi berjaga-jaga jika ada data kosong
df = df.set_index('Year')
df = df.interpolate(method='linear')

# Beri penanda outlier krisis secara eksplisit (sebagai informasi tambahan)
df['is_crisis'] = df.index.isin([1998, 2020]).astype(int)

# 3. PISAHKAN FITUR DAN TARGET
features = ['Inflation', 'Unemployment', 'Population_Growth', 
            'Exports', 'Imports', 'FDI', 'Exchange_Rate', 'is_crisis']
X = df[features]
y = df['GDP_Growth']

# 4. SPLIT DATA (Secara Kronologis untuk Time-Series)
split_idx = int(len(X) * 0.8) # 80% masa lalu untuk belajar, 20% masa depan untuk tes
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
print(f"⚙️  Split data selesai: Train ({len(X_train)}), Test ({len(X_test)})")

# 5. NORMALISASI (SCALING)
os.makedirs('models', exist_ok=True)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test) # Tes HANYA di-transform, tidak di-fit
joblib.dump(scaler, 'models/scaler.pkl')
print("⚖️  Scaler disimpan → models/scaler.pkl")

# 6. DEFINISIKAN 4 MODEL UNTUK DITANDINGKAN
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Decision Tree': DecisionTreeRegressor(max_depth=3, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
}

# 7. LATIH DAN EVALUASI SEMUA MODEL
print("\n🤖 Mulai melatih model...")
results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {'MAE': round(mae, 4), 'RMSE': round(rmse, 4), 'R2': round(r2, 4)}
    print(f"   - {name:<18}: R2 = {r2:+.4f} | MAE = {mae:.4f} | RMSE = {rmse:.4f}")

# Simpan laporan perbandingan model
with open('models/model_report.json', 'w') as f:
    json.dump(results, f, indent=2)
print("📄 Laporan evaluasi disimpan → models/model_report.json")

# 8. PILIH DAN SIMPAN MODEL TERBAIK OTOMATIS
best_name = max(results, key=lambda x: results[x]['R2'])
best_model = models[best_name]
# Latih ulang model terbaik dengan seluruh data (opsional, tapi di sini kita ikuti fit dari train)
best_model.fit(X_train_scaled, y_train) 
joblib.dump(best_model, 'models/best_model.pkl')
print(f"\n🏆 MODEL TERBAIK: {best_name.upper()}!")
print("💾 Model terbaik disimpan → models/best_model.pkl")

# 9. EKSTRAK FEATURE IMPORTANCE (Jika Random Forest / Decision Tree yang menang)
if hasattr(best_model, 'feature_importances_'):
    importance = pd.Series(best_model.feature_importances_, index=features)
    importance = importance.sort_values(ascending=False)
    importance.to_csv('data/processed/feature_importance.csv')
    print("📊 Feature importance disimpan → data/processed/feature_importance.csv")

print("\n" + "="*50 + "\n✅ SELESAI! Seluruh tugas Fauzi sukses dieksekusi.\n" + "="*50)