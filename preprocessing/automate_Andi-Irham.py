import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

def load_data(file_path):
    """
    Memuat dataset dari file CSV.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan di path: {file_path}")
    return pd.read_csv(file_path)

def preprocess_data(df):
    """
    Fungsi otomasi preprocessing dataset Healthcare Cybersecurity.
    Mengambil DataFrame mentah dan mengembalikan DataFrame yang bersih, 
    di-scale, dan di-encode, siap untuk pelatihan model.
    """
    df_clean = df.copy()
    
    # 1. Menangani Data Kosong (Missing Values)
    if 'CVSS_Score' in df_clean.columns:
        median_cvss = df_clean['CVSS_Score'].median()
        df_clean['CVSS_Score'] = df_clean['CVSS_Score'].fillna(median_cvss)
        
    cat_cols = ['Severity', 'Attack_Vector', 'Weakness', 'Status', 'Keyword']
    for col in cat_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna("UNKNOWN")
            
    # 2. Menghapus Data Duplikat
    df_clean = df_clean.drop_duplicates()
    if 'CVE_ID' in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=['CVE_ID'])
        
    # 3. Deteksi dan Penanganan Outlier (IQR Clipping)
    if 'CVSS_Score' in df_clean.columns:
        Q1 = df_clean['CVSS_Score'].quantile(0.25)
        Q3 = df_clean['CVSS_Score'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_clean['CVSS_Score'] = df_clean['CVSS_Score'].clip(lower=lower_bound, upper=upper_bound)
        
    # 4. Normalisasi atau Standarisasi Fitur
    scaler = StandardScaler()
    if 'CVSS_Score' in df_clean.columns:
        df_clean['CVSS_Score_Scaled'] = scaler.fit_transform(df_clean[['CVSS_Score']])
        
    # 5. Encoding Data Kategorikal (One-Hot Encoding)
    cols_to_encode = [col for col in ['Severity', 'Attack_Vector'] if col in df_clean.columns]
    if cols_to_encode:
        df_clean = pd.get_dummies(df_clean, columns=cols_to_encode, drop_first=False)
        
    # 6. Binning (Pengelompokan Data)
    if 'CVSS_Score' in df_clean.columns:
        bins = [-0.1, 3.9, 6.9, 8.9, 10.0]
        labels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        df_clean['CVSS_Risk_Bin'] = pd.cut(df_clean['CVSS_Score'], bins=bins, labels=labels)
        
    return df_clean

def run_pipeline(file_path, output_path=None):
    """
    Fungsi pipeline end-to-end yang memuat lalu memproses data.
    Jika output_path diberikan, data hasil proses akan disimpan ke file CSV.
    """
    df_raw = load_data(file_path)
    df_processed = preprocess_data(df_raw)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_processed.to_csv(output_path, index=False)
        print(f"Data siap latih berhasil disimpan di: {output_path}")
        
    return df_processed

if __name__ == "__main__":
    # Gunakan path relatif terhadap lokasi script ini agar bisa berjalan di OS manapun (termasuk GitHub Actions)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path = os.path.join(base_dir, "healthcare_cybersecurity_raw", "healthcare_cybersecurity_10k.csv")
    out_path = os.path.join(base_dir, "preprocessing", "dataset_preprocessing", "healthcare_cybersecurity_10k_processed.csv")
    
    try:
        df_ready = run_pipeline(test_path, output_path=out_path)
        print("Preprocessing Otomatis Berhasil!")
        print(f"Dimensi data awal vs siap latih: {pd.read_csv(test_path).shape} -> {df_ready.shape}")
    except Exception as e:
        print("Error saat preprocessing:", e)
