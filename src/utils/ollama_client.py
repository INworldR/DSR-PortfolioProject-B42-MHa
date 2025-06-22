"""
Ollama client utilities for the RAG Cybersecurity Classification System.
Provides an interface to the Ollama LLM API for classification and reasoning.
"""

import json
import requests
import time
from typing import Dict, List, Optional, Any
from loguru import logger

from .config import get_config


class OllamaClient:
    """Client for interacting with the Ollama LLM API."""

    def __init__(self, config=None):
        """Initialize the Ollama client with configuration."""
        self.config = config or get_config()
        self.base_url = self.config.ollama_url()
        self.default_model = self.config.OLLAMA_DEFAULT_MODEL
        self.fallback_model = self.config.OLLAMA_FALLBACK_MODEL
        self.timeout = self.config.OLLAMA_TIMEOUT
        self.max_tokens = self.config.OLLAMA_MAX_TOKENS
        self.temperature = self.config.OLLAMA_TEMPERATURE

        logger.info(f"Ollama client initialized with URL: {self.base_url}")

    def test_connection(self) -> bool:
        """Test connection to the Ollama server."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                logger.info(
                    f"Ollama connection successful. Available models: {[m['name'] for m in models.get('models', [])]}"
                )
                return True
            else:
                logger.error(
                    f"Ollama connection failed with status code: {response.status_code}"
                )
                return False
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            return False

    def get_available_models(self) -> List[str]:
        """Get a list of available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                return [m["name"] for m in models.get("models", [])]
            else:
                logger.error(f"Failed to get models: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return []

    def generate(
        self, prompt: str, model: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """Generate a response from the Ollama model."""
        model = model or self.default_model

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }

        try:
            logger.debug(f"Generating with model {model}")
            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                logger.error(
                    f"Generation failed with status code: {response.status_code}"
                )
                return None

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None

    def classify_cybersecurity_log(
        self, log_text: str, context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Classify a cybersecurity log using RAG context."""

        # Build RAG prompt
        prompt = self._build_classification_prompt(log_text, context)

        # Generate classification
        response = self.generate(prompt)

        if response:
            try:
                # Try to parse JSON response
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                logger.warning(
                    "Failed to parse JSON response, attempting to extract manually"
                )
                return self._extract_classification_from_text(response)

        return None

    def _build_classification_prompt(
        self, log_text: str, context: Dict[str, Any]
    ) -> str:
        """Build a classification prompt with RAG context."""

        historical_cases = context.get("historical", [])
        mitre_techniques = context.get("mitre", [])

        prompt = f"""You are a cybersecurity expert specializing in MITRE ATT&CK classification.
You analyze firewall and Apache logs to identify attack techniques.
Always respond in valid JSON format.

Historical Similar Cases:
{json.dumps(historical_cases[:3], indent=2) if historical_cases else "No similar cases found"}

Relevant MITRE Techniques:
{json.dumps(mitre_techniques[:2], indent=2) if mitre_techniques else "No specific techniques found"}

Current Log to Classify:
{log_text}

Based on the context above, classify this log according to MITRE ATT&CK:

Respond in JSON format:
{{
    "technique": "T1046",
    "technique_name": "Network Service Scanning",
    "confidence": 0.87,
    "reasoning": "This log shows...",
    "similar_cases": ["case1", "case2"]
}}"""

        return prompt

    def _extract_classification_from_text(self, text: str) -> Dict[str, Any]:
        """Extract classification from a non-JSON text response."""
        # Fallback parsing for non-JSON responses
        result = {
            "technique": "T1046",  # Default
            "technique_name": "Unknown",
            "confidence": 0.5,
            "reasoning": text,
            "similar_cases": [],
        }

        # Try to extract technique ID
        import re

        technique_match = re.search(r"T\d{4}", text)
        if technique_match:
            result["technique"] = technique_match.group()

        # Try to extract confidence
        confidence_match = re.search(r'confidence["\s:]+([0-9.]+)', text, re.IGNORECASE)
        if confidence_match:
            try:
                result["confidence"] = float(confidence_match.group(1))
            except ValueError:
                pass

        return result

    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the Ollama service."""
        health = {
            "status": "unknown",
            "models": [],
            "connection": False,
            "default_model": self.default_model,
        }

        try:
            # Test connection
            health["connection"] = self.test_connection()

            if health["connection"]:
                health["status"] = "healthy"
                health["models"] = self.get_available_models()

                # Check if default model is available
                if self.default_model in health["models"]:
                    health["default_model_available"] = True
                else:
                    health["default_model_available"] = False
                    health["status"] = "warning"
            else:
                health["status"] = "unhealthy"

        except Exception as e:
            health["status"] = "error"
            health["error"] = str(e)

        return health


def test_ollama_connection():
    """Test Ollama connection and print results."""
    client = OllamaClient()

    print("=== Ollama Connection Test ===")
    print(f"Ollama URL: {client.base_url}")
    print(f"Default Model: {client.default_model}")

    # Test connection
    if client.test_connection():
        print("✅ Connection successful")

        # Get available models
        models = client.get_available_models()
        print(f"Available models: {models}")

        # Health check
        health = client.health_check()
        print(f"Health status: {health['status']}")

    else:
        print("❌ Connection failed")


if __name__ == "__main__":
    test_ollama_connection()
