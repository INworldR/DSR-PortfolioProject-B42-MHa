"""
Configuration management for the RAG Cybersecurity Classification System.
Loads settings from environment variables using pydantic-settings.
"""

from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load environment variables from .env file
load_dotenv()


class Config(BaseSettings):
    # Data Paths
    DATA_DIR: str = Field(default="data")
    RAW_DIR: str = Field(default="data/raw")
    PROCESSED_DIR: str = Field(default="data/processed")

    # ChromaDB
    CHROMADB_HOST: str = Field(default="localhost")
    CHROMADB_PORT: int = Field(default=8000)
    CHROMADB_URL: Optional[str] = None

    # Ollama
    OLLAMA_HOST: str = Field(default="localhost")
    OLLAMA_PORT: int = Field(default=11434)
    OLLAMA_URL: Optional[str] = None
    OLLAMA_DEFAULT_MODEL: str = Field(default="llama3.1:8b")
    OLLAMA_FALLBACK_MODEL: str = Field(default="llama3.1:70b")
    OLLAMA_TIMEOUT: int = Field(default=30)
    OLLAMA_MAX_TOKENS: int = Field(default=2048)
    OLLAMA_TEMPERATURE: float = Field(default=0.1)

    # Streamlit
    STREAMLIT_HOST: str = Field(default="0.0.0.0")
    STREAMLIT_PORT: int = Field(default=8501)
    STREAMLIT_URL: Optional[str] = None

    # App
    LOG_LEVEL: str = Field(default="INFO")
    DEBUG_MODE: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="development")

    class Config:
        env_file = ".env"
        extra = "ignore"

    def get_data_path(self) -> Path:
        return Path(self.DATA_DIR)

    def get_raw_path(self) -> Path:
        return Path(self.RAW_DIR)

    def get_processed_path(self) -> Path:
        return Path(self.PROCESSED_DIR)

    def chromadb_url(self) -> str:
        return self.CHROMADB_URL or f"http://{self.CHROMADB_HOST}:{self.CHROMADB_PORT}"

    def ollama_url(self) -> str:
        return self.OLLAMA_URL or f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}"

    def streamlit_url(self) -> str:
        return (
            self.STREAMLIT_URL or f"http://{self.STREAMLIT_HOST}:{self.STREAMLIT_PORT}"
        )

    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    def is_debug(self) -> bool:
        return self.DEBUG_MODE


# Global config instance
config = Config()


# Convenience functions
def get_config() -> Config:
    return config


def reload_config() -> Config:
    global config
    config = Config()
    return config


def get_data_path() -> Path:
    return config.get_data_path()


def get_raw_path() -> Path:
    return config.get_raw_path()


def get_processed_path() -> Path:
    return config.get_processed_path()


def get_chromadb_url() -> str:
    return config.chromadb_url()


def get_ollama_url() -> str:
    return config.ollama_url()


def get_streamlit_url() -> str:
    return config.streamlit_url()


if __name__ == "__main__":
    print("=== Configuration Test ===")
    print(f"Data Path: {get_data_path()}")
    print(f"Raw Path: {get_raw_path()}")
    print(f"Processed Path: {get_processed_path()}")
    print(f"ChromaDB URL: {get_chromadb_url()}")
    print(f"Ollama URL: {get_ollama_url()}")
    print(f"Streamlit URL: {get_streamlit_url()}")
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Debug Mode: {config.DEBUG_MODE}")
    print(f"Ollama Default Model: {config.OLLAMA_DEFAULT_MODEL}")
