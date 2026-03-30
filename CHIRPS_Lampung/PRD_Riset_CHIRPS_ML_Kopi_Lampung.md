# Product Requirements Document (PRD)
# Prediksi Produktivitas Kopi Robusta Lampung Berbasis Data Satelit CHIRPS dan Machine Learning

| Field | Detail |
|-------|--------|
| **Judul Riset** | Climate-Driven Robusta Coffee Yield Prediction in Lampung, Indonesia: A Machine Learning Approach Using CHIRPS Satellite Precipitation Data |
| **Versi** | 1.0 |
| **Tanggal** | 30 Maret 2026 |
| **Status** | Draft |

---

## 1. Ringkasan Eksekutif

Riset ini bertujuan membangun model prediksi produktivitas kopi Robusta di Provinsi Lampung menggunakan pendekatan machine learning dengan data curah hujan satelit CHIRPS sebagai input utama. Lampung merupakan salah satu sentra kopi Robusta terbesar di Indonesia (~12% dari produksi nasional), namun belum ada studi yang mengkombinasikan data CHIRPS + ML untuk memprediksi produktivitas kopi di wilayah ini. Riset ini mengisi gap tersebut dan berkontribusi pada upaya adaptasi perubahan iklim di sektor perkebunan.

---

## 2. Latar Belakang & Motivasi

### 2.1 Permasalahan
- Produktivitas kopi Robusta Lampung sangat dipengaruhi oleh variabilitas curah hujan
- Perubahan iklim (El Nino, IOD positif) menyebabkan kekeringan yang menurunkan produktivitas
- Stasiun curah hujan BMKG di Lampung sangat terbatas (sparse gauge network)
- Petani dan pemangku kebijakan belum memiliki alat prediksi berbasis data untuk antisipasi gagal panen

### 2.2 Mengapa Sekarang?
- CHIRPS v2.0/v3 menyediakan data curah hujan gridded resolusi tinggi (5 km) sejak 1981
- Ketersediaan data produksi BPS yang semakin terbuka
- Perkembangan ML/DL yang memungkinkan pemodelan hubungan non-linear iklim-produksi
- Belum ada studi serupa untuk Lampung — peluang first-mover

### 2.3 Research Gap
| Studi Sebelumnya | Limitasi | Gap yang Diisi Riset Ini |
|------------------|----------|--------------------------|
| Climatic Suitability for Robusta Coffee in West Lampung (2022) | Hanya pemetaan kesesuaian, bukan prediksi yield | Prediksi kuantitatif produktivitas |
| Projection of Robusta Coffee Climate Suitability (2023) | Proyeksi GCM tanpa data produksi aktual | Validasi dengan data BPS aktual |
| AI-Driven Ensemble Learning Bengawan Solo (2025) | Fokus curah hujan Jawa, bukan pertanian | Aplikasi langsung ke sektor pertanian Lampung |
| Temperature & Rainfall Impacts on Coffee Bean (2021) | Analisis statistik konvensional | Pendekatan ML modern |

---

## 3. Tujuan Riset

### 3.1 Tujuan Utama
Membangun model machine learning untuk memprediksi produktivitas kopi Robusta di Lampung berdasarkan data curah hujan satelit CHIRPS dan variabel iklim pendukung.

### 3.2 Tujuan Spesifik
1. Memvalidasi akurasi data CHIRPS terhadap data stasiun BMKG di wilayah Lampung
2. Menganalisis pengaruh variabilitas curah hujan (termasuk anomali/SPI) terhadap produktivitas kopi Robusta
3. Mengembangkan dan membandingkan performa beberapa model ML (Random Forest, XGBoost, SVR, LSTM) untuk prediksi produktivitas kopi
4. Mengidentifikasi variabel iklim yang paling berpengaruh terhadap produktivitas kopi melalui feature importance analysis
5. Membangun framework early warning system sederhana untuk risiko penurunan produktivitas

### 3.3 Pertanyaan Riset (Research Questions)
- **RQ1:** Seberapa akurat data CHIRPS merepresentasikan pola curah hujan di wilayah perkebunan kopi Lampung?
- **RQ2:** Variabel iklim apa yang paling signifikan mempengaruhi produktivitas kopi Robusta di Lampung?
- **RQ3:** Model ML mana yang paling optimal untuk memprediksi produktivitas kopi berdasarkan data iklim satelit?
- **RQ4:** Dapatkah model yang dibangun digunakan sebagai early warning terhadap risiko penurunan produktivitas?

---

## 4. Hipotesis

- **H1:** Data CHIRPS memiliki korelasi tinggi (r > 0.7) dengan data stasiun BMKG di Lampung pada skala bulanan
- **H2:** Curah hujan pada fase pembungaan (Jun-Aug) dan pematangan buah (Sep-Nov) memiliki pengaruh paling signifikan terhadap produktivitas kopi
- **H3:** Model ensemble (XGBoost/Random Forest) memberikan akurasi prediksi lebih baik dibanding model linier konvensional (R² > 0.75)
- **H4:** Anomali curah hujan negatif (SPI < -1) berkorelasi dengan penurunan produktivitas kopi pada musim panen berikutnya

---

## 5. Metodologi

### 5.1 Kerangka Penelitian

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 1: DATA COLLECTION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CHIRPS v2.0 ──┐                                                │
│  ERA5 ─────────┤                                                │
│  MODIS NDVI ───┼──► Preprocessing ──► Feature Engineering       │
│  ENSO/IOD ─────┤         │                    │                 │
│  DEM SRTM ─────┘         │                    │                 │
│                           ▼                    ▼                │
│                    BMKG Validation      Lag Features             │
│                                         SPI Calculation         │
│                                         Seasonal Aggregation    │
├─────────────────────────────────────────────────────────────────┤
│                    FASE 2: MODELING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Features ──► Train/Test Split ──► Model Training               │
│                  (80/20)              │                          │
│                                       ├── Random Forest         │
│  Target:                              ├── XGBoost               │
│  Produktivitas                        ├── SVR                   │
│  Kopi (kg/ha)                         ├── LSTM                  │
│  (BPS Data)                           └── Linear Regression     │
│                                              (baseline)         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    FASE 3: EVALUATION & ANALYSIS                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Model Comparison ──► Feature Importance ──► Early Warning      │
│  (R², RMSE, MAE)       (SHAP Analysis)       Framework          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Wilayah Studi
- **Utama:** 13 kabupaten/kota di Provinsi Lampung
- **Perluasan (opsional):** Provinsi Sumatera Selatan dan Bengkulu (untuk menambah data points)
- **Bounding box:** 103.5°E - 106.0°E, 3.5°S - 6.0°S
- **Fokus kabupaten produsen kopi utama:**
  - Lampung Barat (~50% produksi kopi Lampung)
  - Tanggamus
  - Lampung Utara
  - Way Kanan

### 5.3 Periode Studi
- **Periode analisis:** 2010-2023 (14 tahun, disesuaikan ketersediaan data BPS)
- **Training set:** 2010-2020 (11 tahun)
- **Test set:** 2021-2023 (3 tahun)
- **Periode CHIRPS untuk klimatologi:** 1981-2023 (untuk baseline SPI)

---

## 6. Kebutuhan Data

### 6.1 Data Primer

| No | Dataset | Sumber | Variabel | Resolusi Spasial | Resolusi Temporal | Periode | Status Akses |
|----|---------|--------|----------|-----------------|-------------------|---------|-------------|
| 1 | **CHIRPS v2.0** | CHC UCSB | Curah hujan (mm) | 0.05° (~5 km) | Bulanan | 1981-2025 | ✅ Gratis, open access |
| 2 | **Data Produksi Kopi** | BPS Lampung | Luas panen (ha), Produksi (ton), Produktivitas (kg/ha) | Per kabupaten | Tahunan | 2010-2023 | ✅ Gratis, online |
| 3 | **Data Stasiun BMKG** | BMKG Data Online / Surat resmi | Curah hujan harian (mm) | Per stasiun | Harian | 2010-2023 | ⚠️ Perlu pengajuan surat |

### 6.2 Data Sekunder

| No | Dataset | Sumber | Variabel | Resolusi | Status |
|----|---------|--------|----------|----------|--------|
| 4 | **ERA5 Reanalysis** | Copernicus CDS | Suhu 2m, kelembaban, evapotranspirasi, SST | 0.25° (~25 km), bulanan | ✅ Gratis |
| 5 | **MODIS NDVI (MOD13A3)** | NASA Earthdata | NDVI, EVI | 1 km, bulanan | ✅ Gratis |
| 6 | **DEM SRTM / DEMNAS** | USGS / BIG | Elevasi, slope | 30m / 8m | ✅ Gratis |
| 7 | **Indeks ENSO** | NOAA CPC | Nino 3.4 SST anomaly | Global index, bulanan | ✅ Gratis |
| 8 | **Indeks IOD** | NOAA/BOM | Dipole Mode Index (DMI) | Global index, bulanan | ✅ Gratis |

### 6.3 Data Opsional (Memperkuat Analisis)

| No | Dataset | Sumber | Fungsi |
|----|---------|--------|--------|
| 9 | Data produksi padi (BPS) | BPS Lampung | Perbandingan dampak iklim lintas komoditas |
| 10 | Data harga kopi | Dinas Pertanian / BPS | Analisis dampak ekonomi |
| 11 | Sentinel-2 imagery | Copernicus | NDVI resolusi tinggi (sejak 2017) |

### 6.4 Estimasi Volume Data

| Dataset | Ukuran Estimasi |
|---------|----------------|
| CHIRPS bulanan Lampung (1981-2025) | ~50 MB (setelah clipping) |
| ERA5 Lampung (2010-2023) | ~200 MB |
| MODIS NDVI Lampung (2010-2023) | ~500 MB |
| DEM SRTM Lampung | ~100 MB |
| Data BPS + BMKG | ~5 MB (tabel CSV) |
| **Total estimasi** | **~1 GB** |

---

## 7. Feature Engineering

### 7.1 Features dari CHIRPS

| Feature | Deskripsi | Justifikasi |
|---------|-----------|-------------|
| `precip_annual` | Total curah hujan tahunan (mm) | Indikator ketersediaan air keseluruhan |
| `precip_wet_season` | CH musim hujan Nov-Mar (mm) | Fase pengisian air tanah |
| `precip_dry_season` | CH musim kering Jun-Sep (mm) | Stress kekeringan saat pembungaan |
| `precip_flowering` | CH fase bunga Jun-Aug (mm) | Periode kritis kopi Robusta |
| `precip_fruiting` | CH fase buah Sep-Nov (mm) | Periode kritis pematangan |
| `dry_spell_max` | Hari kering berturut-turut terpanjang | Intensitas kekeringan |
| `rainy_days` | Jumlah hari hujan (>1mm) per tahun | Distribusi hujan |
| `spi_3` | SPI 3-bulan (Standardized Precipitation Index) | Anomali curah hujan jangka pendek |
| `spi_6` | SPI 6-bulan | Anomali curah hujan jangka menengah |
| `spi_12` | SPI 12-bulan | Anomali curah hujan jangka panjang |
| `precip_cv` | Koefisien variasi CH bulanan | Variabilitas intra-annual |
| `precip_lag1yr` | CH tahun sebelumnya | Efek carry-over terhadap tanaman tahunan |

### 7.2 Features dari ERA5

| Feature | Deskripsi |
|---------|-----------|
| `temp_mean_annual` | Suhu rata-rata tahunan (°C) |
| `temp_max_dry` | Suhu maksimum musim kering (°C) |
| `et0_annual` | Evapotranspirasi potensial tahunan (mm) |
| `humidity_mean` | Kelembaban relatif rata-rata (%) |
| `water_deficit` | Defisit air = ET0 - Curah Hujan (mm) |

### 7.3 Features dari MODIS

| Feature | Deskripsi |
|---------|-----------|
| `ndvi_mean_annual` | NDVI rata-rata tahunan |
| `ndvi_min` | NDVI minimum (indikator stress) |
| `ndvi_anomaly` | Anomali NDVI terhadap rata-rata jangka panjang |
| `evi_mean_growing` | EVI rata-rata musim tumbuh |

### 7.4 Features Lainnya

| Feature | Deskripsi |
|---------|-----------|
| `elevation` | Elevasi rata-rata kabupaten (m dpl) |
| `slope` | Kemiringan lereng rata-rata (°) |
| `nino34` | Indeks ENSO Nino 3.4 rata-rata tahunan |
| `dmi` | Dipole Mode Index rata-rata tahunan |
| `area_harvested` | Luas panen kopi (ha) — kontrol non-iklim |

### 7.5 Target Variable

| Variable | Satuan | Sumber |
|----------|--------|--------|
| **Produktivitas kopi Robusta** | kg/ha | BPS Lampung |

---

## 8. Desain Model

### 8.1 Model yang Akan Diuji

| Model | Tipe | Alasan Dipilih | Hyperparameter Utama |
|-------|------|----------------|---------------------|
| **Linear Regression** | Baseline | Pembanding minimum | - |
| **Random Forest** | Ensemble, bagging | Robust untuk small data, interpretable | n_estimators, max_depth, min_samples_leaf |
| **XGBoost** | Ensemble, boosting | State-of-art untuk tabular data | learning_rate, max_depth, n_estimators, reg_alpha |
| **SVR** | Kernel-based | Baik untuk small sample size | C, epsilon, kernel, gamma |
| **LSTM** | Deep learning (opsional) | Menangkap dependensi temporal | units, layers, dropout, sequence_length |

### 8.2 Strategi Validasi

Mengingat keterbatasan data (~182 data points):

| Metode | Deskripsi |
|--------|-----------|
| **Leave-One-Year-Out CV** | Iterasi: latih dengan semua tahun kecuali satu, uji pada tahun yang ditinggalkan. Cocok untuk data time-series |
| **Spatial K-Fold CV** | Bagi data berdasarkan kabupaten, pastikan tidak ada spatial leakage |
| **Hold-out test set** | 2021-2023 sebagai final test (tidak tersentuh selama tuning) |

### 8.3 Metrik Evaluasi

| Metrik | Formula | Target |
|--------|---------|--------|
| **R²** | Coefficient of determination | > 0.70 |
| **RMSE** | Root Mean Square Error | Semakin rendah semakin baik |
| **MAE** | Mean Absolute Error | Semakin rendah semakin baik |
| **MAPE** | Mean Absolute Percentage Error | < 15% |

### 8.4 Interpretabilitas

| Metode | Fungsi |
|--------|--------|
| **SHAP values** | Menjelaskan kontribusi setiap fitur terhadap prediksi |
| **Partial Dependence Plots** | Visualisasi hubungan fitur-target |
| **Feature Importance** | Ranking variabel iklim paling berpengaruh |

---

## 9. Deliverables & Output

### 9.1 Publikasi

| Output | Target | Status |
|--------|--------|--------|
| Paper utama | *International Journal of Climatology* (Q1) atau *Remote Sensing, MDPI* (Q1) | Prioritas |
| Paper kedua (opsional) | *Agricultural Water Management* (Q1) — fokus aplikasi pertanian | Opsional |

### 9.2 Struktur Paper

```
1. Introduction
   - Climate change impact on coffee production
   - Limitations of ground-based rainfall data in Lampung
   - CHIRPS as alternative + ML opportunity
   - Research gap & objectives

2. Study Area & Data
   - Lampung Province description
   - CHIRPS, ERA5, MODIS, BPS data description
   - BMKG validation data

3. Methodology
   - Data preprocessing & feature engineering
   - SPI calculation
   - ML model descriptions
   - Validation strategy

4. Results
   - CHIRPS validation against BMKG
   - Exploratory analysis: climate-yield relationship
   - Model comparison & performance
   - Feature importance (SHAP)
   - Early warning framework

5. Discussion
   - Key climate drivers for Robusta coffee in Lampung
   - Model strengths & limitations
   - Comparison with previous studies
   - Implications for climate adaptation

6. Conclusion & Recommendations
```

### 9.3 Technical Output

| Output | Deskripsi |
|--------|-----------|
| **Dataset** | Dataset terintegrasi iklim-produksi kopi Lampung (bisa dipublikasi di Zenodo/Mendeley Data) |
| **Source code** | Repository GitHub (Python notebooks) |
| **Trained model** | Model terbaik + pipeline preprocessing |
| **Dashboard (opsional)** | Streamlit app untuk demo early warning |

---

## 10. Timeline

| Fase | Aktivitas | Durasi | Target Selesai |
|------|-----------|--------|---------------|
| **Fase 0** | Literature review & finalisasi desain riset | 2 minggu | Apr 2026 W2 |
| **Fase 1** | Pengumpulan data (CHIRPS, BPS, BMKG, ERA5, MODIS) | 3 minggu | Mei 2026 W1 |
| **Fase 2** | Preprocessing & feature engineering | 2 minggu | Mei 2026 W3 |
| **Fase 3** | Validasi CHIRPS vs BMKG | 1 minggu | Mei 2026 W4 |
| **Fase 4** | Exploratory data analysis | 1 minggu | Jun 2026 W1 |
| **Fase 5** | Model training & tuning | 3 minggu | Jun 2026 W4 |
| **Fase 6** | Evaluasi, SHAP analysis, visualisasi | 2 minggu | Jul 2026 W2 |
| **Fase 7** | Penulisan paper | 4 minggu | Agu 2026 W2 |
| **Fase 8** | Review internal & revisi | 2 minggu | Agu 2026 W4 |
| **Fase 9** | Submission ke jurnal | - | Sep 2026 |
| | **Total** | **~20 minggu (~5 bulan)** | |

---

## 11. Risiko & Mitigasi

| Risiko | Dampak | Probabilitas | Mitigasi |
|--------|--------|-------------|----------|
| Data BMKG sulit diperoleh | Validasi CHIRPS terhambat | Sedang | Gunakan data SACAD BMKG; atau referensikan validasi dari studi sebelumnya di Lampung |
| Data BPS tidak lengkap per kabupaten | Jumlah data points berkurang | Rendah | Perluas ke provinsi tetangga (Sumsel, Bengkulu) |
| Jumlah data terlalu sedikit untuk ML | Model overfitting | Sedang | Gunakan model simple (RF, SVR); tambah data via feature augmentation; gunakan cross-validation ketat |
| Korelasi iklim-produksi lemah | Akurasi model rendah | Rendah-Sedang | Tambahkan faktor non-iklim (luas panen, NDVI); diskusikan limitasi secara jujur di paper |
| Reviewer minta data lebih panjang | Revisi major | Sedang | Siapkan analisis sensitivitas dengan berbagai panjang data |

---

## 12. Tools & Infrastruktur

### 12.1 Software Stack

| Komponen | Tool | Versi |
|----------|------|-------|
| Bahasa pemrograman | Python | 3.10+ |
| Data processing | pandas, numpy, xarray | Latest |
| Geospasial | rasterio, geopandas, rioxarray | Latest |
| ML Framework | scikit-learn, XGBoost | Latest |
| Deep Learning (opsional) | TensorFlow/PyTorch | Latest |
| Interpretabilitas | SHAP | Latest |
| Visualisasi | matplotlib, seaborn, folium | Latest |
| Notebook | Jupyter / Google Colab | Latest |
| Version control | Git + GitHub | Latest |

### 12.2 Infrastruktur Komputasi

| Opsi | Spesifikasi | Biaya |
|------|-------------|-------|
| **Google Colab Pro** | GPU T4/V100, 25 GB RAM | ~Rp 150.000/bulan |
| **Laptop lokal** | CPU cukup untuk RF/XGBoost | Gratis |
| **GPU kampus (jika ada)** | Untuk LSTM training | Gratis |

---

## 13. Estimasi Biaya

| Item | Estimasi Biaya | Keterangan |
|------|---------------|------------|
| Data CHIRPS, ERA5, MODIS, ENSO/IOD | Rp 0 | Open access |
| Data BPS | Rp 0 | Online gratis |
| Data BMKG (jika berbayar) | Rp 0 - 500.000 | Gratis untuk akademik (surat resmi) |
| Google Colab Pro (5 bulan) | Rp 750.000 | Opsional |
| Publication fee (open access) | Rp 0 - 30.000.000 | Tergantung jurnal; banyak yang free |
| **Total estimasi** | **Rp 0 - 31.250.000** | |

**Catatan:** Banyak jurnal Q1/Q2 yang **tidak memungut biaya** (non-APC), seperti *Int. J. of Climatology* (Wiley, hybrid), *Agricultural Water Management* (Elsevier, hybrid). Bisa juga target jurnal full open access gratis seperti *Remote Sensing (MDPI)* dengan waiver.

---

## 14. Kriteria Keberhasilan

| Kriteria | Target | Prioritas |
|----------|--------|-----------|
| Paper diterima di jurnal Q1/Q2 terindeks Scopus | 1 paper | Utama |
| Model prediksi dengan R² > 0.70 | Tercapai | Utama |
| Identifikasi variabel iklim kunci | Top-5 features | Utama |
| Dataset publik di Zenodo | 1 dataset | Sekunder |
| Source code di GitHub | 1 repository | Sekunder |
| Dashboard early warning (Streamlit) | 1 prototype | Opsional |

---

## 15. Referensi Utama

1. Funk, C., et al. (2015). The climate hazards infrared precipitation with stations. *Scientific Data*, 2, 150066.
2. Marzuki, et al. (2025). Long-term spatial-temporal variability over Indonesia based on 43 years of CHIRPS data. *Int. J. of Climatology*.
3. Pratama & Agiel (2022). Evaluasi satellite precipitation product di Kabupaten Lampung Selatan.
4. Projection of Robusta coffee climate suitability (2023). *IJSDP*.
5. Crop yield prediction review using ML and DL (2024). *Heliyon*.

---

*Dokumen ini bersifat living document dan akan diperbarui seiring perkembangan riset.*
