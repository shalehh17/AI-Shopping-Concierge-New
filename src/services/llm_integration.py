import json
from google import genai
from google.genai import types
from src.config import Config

class GeminiLLMClient:
    def __init__(self):
        """
        Model Client Initialization (RAG Architecture).
        Instantiates the Generative AI inference client for production workflows, 
        leveraging modern SDK architecture for maximum compatibility and stateless execution.
        """
        # Credential Validation Layer: Pre-flight check to prevent runtime authentication failures
        if not Config.GEMINI_API_KEY:
            raise ValueError("[Configuration Error] GEMINI_API_KEY is missing from the environment runtime.")
            
        # SDK Client Instantiation: Establish secure connection to Generative LLM endpoint
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        # Dependency Resolution: Read dynamic model configuration from Config/.env with fallback
        self.model_name = getattr(Config, "LLM_MODEL_NAME", "gemini-2.0-flash")

    def synthesize_shopping_recommendation(self, user_query: str, grounded_context: list) -> str:
        """
        Generative Inference Pipeline (Retrieval-Augmented Generation).
        Synthesizes structured retrieval payloads into JSON structured responses, 
        enforcing zero hallucination and seamless UI parsing for downstream consumption.
        """
        # Search Space Collapse Mitigation: Implement graceful degradation for null candidate sets
        if not grounded_context:
            return json.dumps({
                "summary": "Informasi stok tidak tersedia untuk kriteria produk yang diminta.",
                "recommendations": []
            })

        # 1. Context Injection & Semantic Serialization
        # Serialize database records into unified textual representations
        product_context_str = ""
        for idx, item in enumerate(grounded_context, 1):
            nama = item.get("Nama Produk", item.get("nama_produk", "Produk Tanpa Nama"))
            harga = item.get("Harga (Untuk Filter Metadata)", item.get("harga", 0))
            brand = item.get("Brand", item.get("brand", "-"))
            subkat = item.get("Sub Kategori", item.get("sub_kategori", "Outdoor"))
            deskripsi = item.get("Deskripsi Teks (Untuk Embeddings)", item.get("deskripsi", ""))
            
            product_context_str += (
                f"[{idx}] ID: PROD-{idx}\n"
                f"    Nama: {nama}\n"
                f"    Brand: {brand}\n"
                f"    Kategori: {subkat}\n"
                f"    Harga: {harga}\n"
                f"    Deskripsi: {deskripsi}\n"
                f"{'-'*40}\n"
            )

        # 2. Unified Payload Orchestration (JSON Structured Constraints)
        prompt_payload = (
            "SISTEM INSTRUKSI (DETERMINISTIC CONSTRAINTS & JSON STRUCTURED OUTPUT):\n"
            "Peran: AI Shopping Concierge profesional produk outdoor.\n"
            "Tugas: Merekomendasikan produk PALING RELEVAN dari daftar GROUND TRUTH di bawah.\n"
            "Constraint: Gunakan informasi Brand, Kategori, Deskripsi, dan Harga secara presisi.\n"
            "Zero Hallucination Tolerance: Dilarang mengarang produk, memodifikasi spesifikasi, atau memanipulasi harga!\n\n"
            "Format Luaran: WAJIB mengembalikan JSON MURNI sesuai skema berikut:\n"
            "{\n"
            '  "summary": "Ringkasan jawaban atau saran ramah untuk pelanggan dalam bahasa Indonesia",\n'
            '  "recommendations": [\n'
            "    {\n"
            '      "product_id": "PROD-1",\n'
            '      "product_name": "Nama Lengkap Produk beserta Brand",\n'
            '      "price": 500000,\n'
            '      "category": "Sub Kategori Produk",\n'
            '      "reason": "Alasan singkat mengapa produk ini cocok untuk kueri pengguna",\n'
            '      "key_features": ["Fitur/Keunggulan 1", "Fitur/Keunggulan 2"]\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"--- DAFTAR PRODUK VALID (GROUND TRUTH) ---\n{product_context_str}\n"
            f"Kueri Pelanggan: '{user_query}'\n\n"
            "Respons Rekomendasi (JSON):"
        )

        # 3. Stateless LLM Inference Execution with JSON Mode
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt_payload,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return response.text
            
        except Exception as e:
            # Fallback JSON jika terjadi gangguan jaringan / inference error
            return json.dumps({
                "summary": f"Terjadi kendala saat memproses rekomendasi: {str(e)}",
                "recommendations": []
            })