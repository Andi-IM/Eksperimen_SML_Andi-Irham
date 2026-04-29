# Healthcare Cybersecurity Dataset Preprocessing Automation

Proyek ini menyediakan *pipeline* ETL (Extract, Transform, Load) otomatis untuk memproses raw dataset cybersecurity di bidang kesehatan (Healthcare Cybersecurity). *Pipeline* ini bertujuan untuk membersihkan, menstandarisasi, dan menyiapkan data mentah agar siap digunakan untuk pelatihan model *Machine Learning*.

## Fitur dan Tahapan Preprocessing

Script preprocessing (`preprocessing/automate_Andi-Irham.py`) melakukan beberapa tahapan penting:

1. **Penanganan Data Kosong (Missing Values)**: Mengisi nilai kosong pada kolom numerik (`CVSS_Score`) dengan nilai median, dan mengisi nilai kosong pada kolom kategorikal (`Severity`, `Attack_Vector`, `Weakness`, `Status`, `Keyword`) dengan label "UNKNOWN".
2. **Penghapusan Data Duplikat**: Menghapus baris duplikat, dengan pengecekan spesifik pada kolom unik seperti `CVE_ID`.
3. **Deteksi dan Penanganan Outlier**: Menggunakan metode *IQR (Interquartile Range) Clipping* untuk membatasi nilai *outlier* pada `CVSS_Score`.
4. **Normalisasi / Standarisasi Fitur**: Menggunakan `StandardScaler` untuk menskalakan `CVSS_Score` agar memiliki distribusi standar.
5. **Encoding Data Kategorikal**: Menerapkan *One-Hot Encoding* untuk mengubah data kategorikal (`Severity` dan `Attack_Vector`) menjadi representasi numerik biner.
6. **Binning (Pengelompokan Data)**: Mengelompokkan `CVSS_Score` ke dalam kategori tingkat risiko keamanan (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).

## Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python >= 3.12
- **Library**: `pandas`, `scikit-learn`, `numpy`
- **Package Manager**: `uv` (sangat cepat dan efisien)
- **CI/CD**: GitHub Actions

## Struktur Proyek Utama

- `healthcare_cybersecurity_raw/`: Direktori untuk menyimpan raw dataset.
- `preprocessing/automate_Andi-Irham.py`: Skrip utama yang menjalankan seluruh logika *preprocessing*.
- `preprocessing/dataset_preprocessing/`: Direktori output tempat dataset yang sudah bersih disimpan.
- `.github/workflows/preprocess_data.yml`: Konfigurasi GitHub Actions untuk mengotomatisasi jalannya pipeline.
- `pyproject.toml`: File konfigurasi proyek dan daftar *dependencies*.

## Cara Penggunaan

### Menjalankan secara Lokal

1. Pastikan Anda telah menginstal `uv` (Python Package Manager).
2. Instal semua *dependencies* proyek:
   ```bash
   uv sync
   ```
3. Jalankan skrip preprocessing:
   ```bash
   uv run preprocessing/automate_Andi-Irham.py
   ```
   Skrip akan membaca dataset dari folder raw, memprosesnya, dan menyimpan file `.csv` yang sudah bersih ke dalam `preprocessing/dataset_preprocessing/healthcare_cybersecurity_10k_processed.csv`.

### Otomatisasi CI/CD (GitHub Actions)

Proyek ini telah dilengkapi dengan integrasi *Continuous Integration / Continuous Deployment* (CI/CD) menggunakan **GitHub Actions**. Pipeline preprocessing data (`Data Preprocessing Pipeline`) akan dijalankan secara otomatis jika ada *push* atau *pull request* yang memodifikasi:
- Direktori `healthcare_cybersecurity_raw/**` (Dataset baru)
- File `preprocessing/automate_Andi-Irham.py` (Logika preprocessing)

**Hasil Output (Artifacts)**:
Setiap kali pipeline GitHub Actions selesai dijalankan dengan sukses, ia akan **mengembalikan dataset yang sudah dipreprocess sebagai Artifact baru**. 

**Cara Mengunduh Hasil Preprocessing**:
1. Buka tab **Actions** pada repository GitHub ini.
2. Klik pada run pipeline terbaru (misalnya, *Data Preprocessing Pipeline*).
3. Scroll ke bagian paling bawah pada halaman detail run tersebut.
4. Pada bagian **Artifacts**, klik **`preprocessed-dataset`** untuk mengunduh file `.csv` hasil *preprocessing*. (Artifact ini akan disimpan dan tersedia untuk diunduh selama 7 hari).
