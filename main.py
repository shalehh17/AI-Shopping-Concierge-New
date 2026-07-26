import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.config import Config
from src.services.concierge_pipeline import AIConciergePipeline

# 1. Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="🛒 AI Shopping Concierge - Enterprise Backend API",
    description="Backend API berbasis RAG Commerce Platform untuk ekstraksi entitas pintar dan rekomendasi produk outdoor.",
    version="1.0.0"
)

# 2. CORS Middleware - Mengizinkan Streamlit UI mengakses API ini dari domain/port manapun
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi Variabel Pipeline Global
pipeline = None

# 3. Startup Event Validation Engine (Cold-Start Guard)
@app.on_event("startup")
def configure_startup():
    global pipeline
    try:
        # Menjalankan validasi kredensial (.env / variabel lingkungan Supabase & Gemini)
        Config.validate_config()
        print("="*60)
        print("🤖 AI SHOPPING CONCIERGE ENGINE v1.0 - PRODUCTION ONLINE")
        print("="*60)
        print("[Sistem] Menginisialisasi komponen logika kognitif & database...")
        
        # Mengunci inisialisasi pipeline tunggal (Singleton pattern di API layer)
        pipeline = AIConciergePipeline()
        print("[Sistem] API Server siap menerima request komersial.")
        print("="*60 + "\n")
    except ValueError as e:
        print(f"\n[Gagal Cold-Start Web API] {str(e)}")
        sys.exit(1)

# 4. Pydantic Schema Definition (Validasi Data Masuk)
class CustomerQueryRequest(BaseModel):
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Cari jaket Eiger waterproof budget maksimal 1 juta"
            }
        }

# 5. Endpoint Root - Pengecekan Kesehatan Server (Health Check)
@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "Healthy",
        "service": "AI Shopping Concierge Engine API",
        "production_ready": True
    }

# 6. Endpoint Utama - RAG Inference Pipeline (POST HTTP)
@app.post("/api/recommend", tags=["Core Commerce Inference"])
def process_recommendation(payload: CustomerQueryRequest):
    """
    End-to-End Inference API Endpoint:
    Menerima kueri kasual, mengekstrak entitas via NLU (Gemini JSON Mode), 
    melakukan Hybrid Retrieval ke Supabase, dan mengembalikan 3 produk terbaik beserta teks respons.
    """
    global pipeline
    if not pipeline:
        raise HTTPException(status_code=503, detail="Inference engine tidak terinisialisasi dengan benar di server.")
    
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Kueri pelanggan tidak boleh kosong.")
        
    try:
        # Menjalankan proses pipeline RAG dinamis Anda
        response_payload = pipeline.process_customer_request(payload.query)
        return response_payload
        
    except Exception as e:
        # Menangkap runtime error sistem agar server API tidak mati total
        raise HTTPException(
            status_code=500, 
            detail=f"Terjadi kegagalan komputasi internal sistem API: {str(e)}"
        )
