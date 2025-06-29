"""
RAG-Enhanced Cybersecurity Classification Demo
Streamlit web interface for the RAG system.
"""

import streamlit as st
import sys
import os
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.utils.config import get_config, get_streamlit_url
from src.utils.llm_client import LLMClient
from src.utils.chromadb_client import ChromaDBClient

# Page config
st.set_page_config(
    page_title="RAG Cybersecurity Classification", page_icon="🛡️", layout="wide"
)


def main():
    """Main Streamlit application."""

    st.title("🛡️ RAG-Enhanced Cybersecurity Classification")
    st.markdown("---")

    # Display Streamlit URL
    streamlit_url = get_streamlit_url()
    st.sidebar.markdown(f"**App URL:** {streamlit_url}")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Health checks
        st.subheader("Service Status")

        # LLM health check
        try:
            llm_client = LLMClient()
            llm_health = llm_client.health_check()

            if llm_health["status"] == "healthy":
                st.success("✅ LLM: Connected")
                st.write(f"Models: {len(llm_health['models'])}")
            else:
                st.error("❌ LLM: Disconnected")
        except Exception as e:
            st.error(f"❌ LLM: Error - {e}")

        # ChromaDB health check
        try:
            chromadb_client = ChromaDBClient()
            chromadb_health = chromadb_client.health_check()

            if chromadb_health["status"] == "healthy":
                st.success("✅ ChromaDB: Connected")
                st.write(f"Collections: {len(chromadb_health['collections'])}")
            else:
                st.error("❌ ChromaDB: Disconnected")
        except Exception as e:
            st.error(f"❌ ChromaDB: Error - {e}")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Log Classification")

        # Input area
        log_text = st.text_area(
            "Enter firewall or Apache log entry:",
            height=150,
            placeholder="Example: 192.168.1.100 - - [22/Jun/2025:10:30:45 +0000] 'GET /admin HTTP/1.1' 404 1234",
        )

        if st.button("🔍 Classify Log", type="primary"):
            if log_text.strip():
                with st.spinner("Analyzing log entry..."):
                    try:
                        # Simple classification (placeholder)
                        result = {
                            "technique": "T1046",
                            "technique_name": "Network Service Scanning",
                            "confidence": 0.87,
                            "reasoning": "This log shows a request to /admin endpoint which is commonly scanned by attackers.",
                            "similar_cases": ["admin_scan_001", "port_scan_002"],
                        }

                        st.success("✅ Classification complete!")

                        # Display results
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("MITRE Technique", result["technique"])
                            st.metric("Confidence", f"{result['confidence']:.2%}")

                        with col_b:
                            st.write("**Technique Name:**", result["technique_name"])
                            st.write("**Reasoning:**", result["reasoning"])

                        # Similar cases
                        if result["similar_cases"]:
                            st.subheader("Similar Cases")
                            for case in result["similar_cases"]:
                                st.write(f"- {case}")

                    except Exception as e:
                        st.error(f"Classification failed: {e}")
            else:
                st.warning("Please enter a log entry to classify.")

    with col2:
        st.header("Quick Stats")

        # Placeholder stats
        st.metric("Logs Analyzed", "1,234")
        st.metric("Threats Detected", "56")
        st.metric("False Positives", "3")
        st.metric("Accuracy", "94.5%")

        st.header("Recent Activity")
        st.write("• Log classified: T1046")
        st.write("• New threat pattern detected")
        st.write("• Model confidence: 87%")


if __name__ == "__main__":
    main()
