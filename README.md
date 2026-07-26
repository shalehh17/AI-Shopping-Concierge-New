# 🛍️ AI Shopping Concierge — Enterprise RAG Commerce Platform

Aplikasi *Conversational Commerce* modern berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk memberikan pengalaman belanja interaktif peralatan *outdoor*. Platform ini menggabungkan kecerdasan **Google Gemini 2.0**, penelusuran katalog terstruktur, manajemen keranjang belanja (*multi-item cart*), serta kalkulasi checkout finansial yang tervalidasi secara presisi.

---

## 🌟 Fitur Utama

### 1. 💬 Conversational RAG Chatroom
* **Semantic Product Search**: Menerjemahkan kueri bebas pelanggan (*misal: "sepatu gunung", "matras untuk naik gunung"*) menjadi pencarian produk presisi.
* **Deterministic JSON Structured Output**: Menjamin respons AI bebas dari halusinasi (*zero hallucination*) dan dikembalikan dalam format JSON terstruktur.
* **Dynamic Product Cards**: Merender otomatis luaran AI menjadi kartu rekomendasi produk lengkap dengan identitas barang, spesifikasi, alasan rekomendasi, dan gambar produk.

### 2. 🛒 Advanced Cart & Checkout Gateway
* **Multi-Item Cart Management**: Menampung banyak produk sekaligus ke dalam keranjang belanja (`st.session_state.cart`) dengan notifikasi *toast* real-time.
* **SymPy Financial Engine**: Menghitung total transaksi, kuantitas produk, dan biaya ongkos kirim secara matematis melalui kalkulasi SymPy yang tervalidasi.
* **Multi-Payment Settlement**: Simulasi gateway pembayaran interaktif mendukung protokol **QRIS Dinamis**, **Virtual Account (BCA/Mandiri)**, dan **E-Wallet (GoPay/OVO/Dana)**.

### 3. 📊 Observability & Analytics Dashboard (Sidebar)
* **CNN 1D Performance Engine**: Pemantauan estimasi performa arsitektur NLU CNN 1D secara *real-time* berbasis token kueri (*Accuracy & Loss per Epoch*).
* **Financial Payment Log**: Pencatatan logistik transaksi permanen berbasis tabel (*Dataframe*).
* **Clustering Preferensi Pembayaran**: Visualisasi preferensi metode pembayaran pengguna berbasis persentase distribusi.

---

## 🛠️ Teknologi & Modul Utama

| Komponen | Teknologi |
| :--- | :--- |
| **Frontend UI/UX** | Streamlit |
| **Generative LLM Engine** | Google GenAI SDK (`gemini-2.0-flash` / `gemini-2.0-flash-lite`) |
| **Database & Vector Store** | Supabase (PostgreSQL Protocol) |
| **Validation Engine** | SymPy (Financial Formula Evaluation) |
| **Data Processing** | Pandas, NumPy, Python-Dotenv |

---

## 📁 Struktur Direktori Proyek

```text
AI-Shopping-Concierge-New/
├── app.py                      # Main Entry Point & User Interface (Streamlit)
├── config.py                   # Centralized Environment Configuration & Validation
├── .env.example                # Template Variabel Lingkungan
├── .gitignore                  # Git Exclusion Rules (Pencegahan Kebocoran API Key)
├── requirements.txt            # Dependency Management
├── README.md                   # Dokumentasi Proyek
└── src/
    ├── services/
    │   ├── concierge_pipeline.py  # Orchestration Pipeline RAG
    │   └── llm_integration.py     # Gemini LLM Client Integration





🚀 Panduan Instalasi & Penggunaan
1. Prasyarat
Pastikan komputer Anda telah terinstal Python 3.10 atau versi yang lebih baru.

2. Clone Repositori
Bash
git clone [https://github.com/shalehh17/AI-Shopping-Concierge-New.git](https://github.com/shalehh17/AI-Shopping-Concierge-New.git)
cd AI-Shopping-Concierge-New
3. Buat & Aktifkan Virtual Environment
Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
Linux/macOS:

Bash
python3 -m venv venv
source venv/bin/activate
4. Instal Dependensi
Bash
pip install -r requirements.txt
5. Konfigurasi Variabel Lingkungan (.env)
Buat file bernama .env pada folder utama proyek, lalu isi dengan format berikut:

Cuplikan kode
# Kredensial Resmi Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL_NAME=gemini-2.0-flash-lite
GEMINI_API_VERSION=v1beta

# Kredensial Database Supabase
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
SUPABASE_URL=[https://xxx.supabase.co](https://xxx.supabase.co)
SUPABASE_KEY=your_supabase_anon_key_here
6. Jalankan Aplikasi
Bash
streamlit run app.py
Aplikasi akan otomatis berjalan di peramban web pada alamat http://localhost:8501.

👤 Penulis
GitHub: @shalehh17
