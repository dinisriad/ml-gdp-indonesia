# Exploratory Data Analysis (EDA) Summary

## 📌 Temuan Utama
1. **Rata-rata Pertumbuhan:** GDP Growth Indonesia berada di kisaran 5% per tahun pada kondisi normal.
2. **Korelasi Negatif Kuat:** Inflasi memiliki korelasi negatif yang sangat kuat dengan GDP. Jika inflasi naik tajam, GDP akan turun.
3. **Anomali Ekstrem (Outlier):** Terdapat dua titik kontraksi hebat:
   - **Tahun 1998 (-13.1%):** Efek domino dari Krisis Moneter Asia.
   - **Tahun 2020 (-2.07%):** Efek berhentinya aktivitas ekonomi akibat Pandemi COVID-19.

## 💡 Rekomendasi Modeling
Karena keberadaan anomali krisis pada tahun 1998 dan 2020 sangat merusak tren linearitas, pembuatan fitur tambahan seperti `is_crisis` (0 atau 1) sangat direkomendasikan untuk membantu model AI membedakan tahun normal dan tahun bencana.
