import sys
from src.config import Config
from src.services.concierge_pipeline import AIConciergePipeline

def start_chatbot():
    # 1. Lapisan Validasi Awal Kredensial Lingkungan di RAM
    try:
        Config.validate_config()
    except ValueError as e:
        print(f"\n[Gagal Cold-Start] {str(e)}")
        sys.exit(1)

    print("="*60)
    print("🤖 AI SHOPPING CONCIERGE ENGINE v1.0 - PRODUCTION ONLINE")
    print("="*60)
    print("Ketik 'keluar' atau 'exit' untuk menghentikan sesi percakapan.\n")
    
    # 2. Memuat Seluruh Pipeline Orkestrasi Penuh ke RAM
    print("[Sistem] Menginisialisasi komponen logika kognitif & database...")
    concierge = AIConciergePipeline()
    print("[Sistem] AI Concierge siap melayani pelanggan.")
    print("="*60 + "\n")
    
    # 3. Loop Percakapan Real-Time Tanpa Henti
    while True:
        try:
            user_input = input("Pelanggan: ")
            if user_input.lower().strip() in ['keluar', 'exit', 'quit']:
                print("\nAI Concierge: Sesi asisten belanja diakhiri. Sampai jumpa!")
                break
                
            if not user_input.strip():
                continue
                
            # Proses Kueri melalui Pipeline Hibrida (Supabase) + LLM (Gemini)
            response = concierge.process_customer_request(user_input)
            print(f"\nAI Concierge:\n{response}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\nSesi diputus secara paksa. Sampai jumpa!")
            break
        except Exception as e:
            print(f"\n[Runtime Error] Terjadi kegagalan sistem: {str(e)}\n")

if __name__ == "__main__":
    start_chatbot()