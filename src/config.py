import os
from dotenv import load_dotenv

# Environment Provisioning: Ingest configuration parameters with explicit override
load_dotenv(override=True)

class Config:
    """
    Centralized Configuration Management.
    Handles secure ingestion of cloud infrastructure credentials and generative model 
    hyperparameters. Ensures deterministic environment state for reliable pipeline execution.
    """
    
    # Infrastructure Credentials: Cloud relational database and service endpoints
    DATABASE_URL = os.getenv("DATABASE_URL")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_KEY")
    
    # Generative AI Credentials: API keys and model identification for inference
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemini-1.5-flash-latest")
    GEMINI_API_VERSION = os.getenv("GEMINI_API_VERSION", "v1beta")

    @classmethod
    def validate_config(cls):
        """
        Pre-flight Configuration Validation Layer.
        Performs a strict dependency audit of mission-critical environment variables 
        to prevent runtime failures in downstream inference components.
        """
        # Define mandatory environment variables for operational integrity
        required_vars = {
            "SUPABASE_URL": cls.SUPABASE_URL,
            "SUPABASE_KEY": cls.SUPABASE_KEY or cls.SUPABASE_PUBLISHABLE_KEY,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY
        }
        
        # Dependency Audit: Detect absent configuration keys
        missing_vars = [var_name for var_name, value in required_vars.items() if not value]
        
        if missing_vars:
            # Fatal Exception: Halt pipeline execution immediately to ensure system stability
            raise ValueError(
                f"🚨 Fatal Dependency Error: Mission-critical environment variables "
                f"{missing_vars} are missing from the .env configuration. Pipeline execution halted."
            )