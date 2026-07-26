import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Muat variabel lingkungan dari file .env
load_dotenv()

# 2. Ambil kredensial dari environment variable
raw_url = os.getenv("SUPABASE_URL", "")
raw_key = (
    os.getenv("SUPABASE_KEY") 
    or os.getenv("SUPABASE_KEY") 
    or os.getenv("SUPABASE_ANON_KEY") 
    or ""
)

# 3. Sanitasi Karakter: Hapus spasi dan tanda petik ekstra yang tidak sengaja terbawa
SUPABASE_URL = raw_url.strip().strip("'\"")
SUPABASE_KEY = raw_key.strip().strip("'\"")

# 4. Validasi Keberadaan Kredensial
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "❌ [Configuration Error] Kredensial SUPABASE_URL atau SUPABASE_KEY kosong!\n"
        "Pastikan file .env berada di direktori utama proyek dan berisi kredensial yang valid."
    )

# 5. Inisialisasi Client Supabase
try:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Koneksi client ke database Supabase berhasil diinisialisasi.")
except Exception as e:
    key_preview = SUPABASE_KEY[:10] + "..." if len(SUPABASE_KEY) > 10 else SUPABASE_KEY
    raise RuntimeError(
        f"❌ Gagal menginisialisasi client Supabase: {str(e)}\n"
        f"👉 URL Terbaca: '{SUPABASE_URL}'\n"
        f"👉 Key Terbaca (Awalan): '{key_preview}' (Panjang: {len(SUPABASE_KEY)} karakter)\n"
        "💡 Solusi: Pastikan kunci di .env adalah 'anon' public / publishable key yang diawali dengan 'eyJ...'"
    )