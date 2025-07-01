# \!/usr/bin/env python3
"""
Streamlit Demo Interface for ATP Log Generator.

Provides copy-paste functionality for portfolio demonstration.

Author: DSR Portfolio Project Team
"""

import sys
import json
import streamlit as st
from datetime import datetime

sys.path.append(".")
from utils.logger import setup_logger
from atp_log_generator import ATPLogGenerator

logger = setup_logger()


def main():
    """Main Streamlit application."""
    st.title("ATP Log Generator - Portfolio Demo")
    st.write("Generate realistic MITRE ATT&CK attack simulation logs")

    # Initialize generator
    if "generator" not in st.session_state:
        st.session_state.generator = ATPLogGenerator()
        logger.info("ATP Log Generator initialized for Streamlit")

    # APT Group selection
    apt_groups = ["apt29_cozy_bear", "apt1_comment_crew", "lazarus_group"]
    selected_apt = st.selectbox("Select APT Group:", apt_groups)

    # Number of logs
    num_logs = st.slider("Number of logs to generate:", 1, 20, 5)

    # Generate button
    if st.button("Generate ATP Logs"):
        with st.spinner("Generating attack simulation logs..."):
            logs = st.session_state.generator.generate_attack_sequence(
                selected_apt, num_logs
            )
            st.session_state.generated_logs = logs
            logger.info(f"Generated {len(logs)} logs for {selected_apt} via Streamlit")

    # Display results
    if "generated_logs" in st.session_state:
        st.subheader("Generated ATP Logs")

        # Summary
        logs = st.session_state.generated_logs
        st.write(f"Generated {len(logs)} logs for **{logs[0]['apt_group']}**")

        # Techniques used
        techniques = list(
            set(
                [log["mitre_technique"] + " - " + log["technique_name"] for log in logs]
            )
        )
        st.write("**MITRE ATT&CK Techniques:**")
        for technique in techniques:
            st.write(f"- {technique}")

        # JSON output for copy-paste
        st.subheader("JSON Output (Copy-Paste Ready)")
        json_output = json.dumps(logs, indent=2)
        st.code(json_output, language="json")

        # Individual log details
        st.subheader("Log Details")
        for i, log in enumerate(logs, 1):
            with st.expander(
                f"Log {i}: {log['mitre_technique']} - {log['technique_name']}"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Timestamp:** {log['timestamp']}")
                    st.write(f"**Tactic:** {log['tactic']}")
                    st.write(f"**Severity:** {log['severity']}")
                    st.write(f"**Process:** {log['process_name']}")
                    st.write(f"**Success:** {log['success']}")

                with col2:
                    st.write(f"**Source IP:** {log['source_ip']}")
                    st.write(f"**Target:** {log['target_host']}")
                    st.write(f"**Threat Score:** {log['threat_score']}/10")
                    st.write(f"**Confidence:** {log['detection_confidence']}")
                    st.write(f"**Indicators:** {', '.join(log['indicators'])}")

                st.write(f"**Command Line:**")
                st.code(log["command_line"])

    # ChromaDB Integration section
    st.sidebar.header("ChromaDB Integration")
    st.sidebar.write("Integration with existing ChromaDB for RAG queries")

    if st.sidebar.button("Test ChromaDB Integration"):
        st.sidebar.info(
            "ChromaDB integration test - implement with test_chromadb_injection.py"
        )

    # Portfolio Info
    st.sidebar.header("Portfolio Demo")
    st.sidebar.write("DSR Portfolio Project B42-MHa")
    st.sidebar.write("Cybersecurity RAG System")
    st.sidebar.write("MITRE ATT&CK Integration")


if __name__ == "__main__":
    main()
