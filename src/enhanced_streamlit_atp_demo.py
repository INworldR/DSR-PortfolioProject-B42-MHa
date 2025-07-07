#!/usr/bin/env python3

import sys
import json
import streamlit as st
from datetime import datetime

sys.path.append(".")
from utils.logger import setup_logger
from atp_log_generator import ATPLogGenerator
from realistic_atp_generator import RealisticATPGenerator

logger = setup_logger()


def main():
    st.title("ATP Log Generator - Portfolio Demo")
    st.write("Generate realistic MITRE ATT&CK attack simulation logs")

    # Generator selection
    use_realistic = st.checkbox("Use ChromaDB-based realistic values", value=True)

    if "generator" not in st.session_state:
        if use_realistic:
            st.session_state.generator = RealisticATPGenerator()
            st.success("Realistic generator with ChromaDB integration loaded")
        else:
            st.session_state.generator = ATPLogGenerator()
            st.info("Standard generator with simulated values loaded")
        logger.info("ATP Log Generator initialized for Streamlit")

    # APT Group selection
    apt_groups = ["apt29_cozy_bear", "apt1_comment_crew", "lazarus_group"]
    selected_apt = st.selectbox("Select APT Group:", apt_groups)

    # Number of logs
    num_logs = st.slider("Number of logs to generate:", 1, 20, 5)

    # Generate button
    if st.button("Generate ATP Logs"):
        with st.spinner("Generating attack simulation logs..."):
            if use_realistic:
                logs = st.session_state.generator.generate_realistic_logs(
                    selected_apt, num_logs, "./data/chromadb"
                )
                st.success(
                    f"Generated {len(logs)} logs with ChromaDB-based confidence values"
                )
            else:
                logs = st.session_state.generator.generate_attack_sequence(
                    selected_apt, num_logs
                )
                st.info(f"Generated {len(logs)} logs with simulated values")

            st.session_state.generated_logs = logs
            logger.info(f"Generated {len(logs)} logs for {selected_apt} via Streamlit")

    # Display results
    if "generated_logs" in st.session_state:
        st.subheader("Generated ATP Logs")

        logs = st.session_state.generated_logs
        if logs:
            st.write(f"Generated {len(logs)} logs for **{logs[0]['apt_group']}**")
        else:
            st.warning("No logs generated - check APT group configuration")
            return

        # Confidence analysis
        if logs:
            avg_confidence = sum(log["detection_confidence"] for log in logs) / len(
                logs
            )
            avg_fp_rate = sum(log["false_positive_probability"] for log in logs) / len(
                logs
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Avg Detection Confidence", f"{avg_confidence:.2f}")
            with col2:
                st.metric("Avg False Positive Rate", f"{avg_fp_rate:.2f}")

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
            confidence_color = (
                "🟢"
                if log["detection_confidence"] > 0.8
                else "🟡" if log["detection_confidence"] > 0.6 else "🔴"
            )
            fp_color = (
                "🟢"
                if log["false_positive_probability"] < 0.15
                else "🟡" if log["false_positive_probability"] < 0.25 else "🔴"
            )

            with st.expander(
                f"Log {i}: {log['mitre_technique']} - {log['technique_name']} {confidence_color}"
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
                    st.write(
                        f"**Confidence:** {log['detection_confidence']} {confidence_color}"
                    )
                    st.write(
                        f"**FP Rate:** {log['false_positive_probability']} {fp_color}"
                    )

                st.write(f"**Indicators:** {', '.join(log['indicators'])}")
                st.write(f"**Command Line:**")
                st.code(log["command_line"])

    # ChromaDB Integration section
    st.sidebar.header("ChromaDB Integration Status")
    if st.sidebar.button("Test ChromaDB Connection"):
        try:
            import chromadb

            client = chromadb.PersistentClient(path="./data/chromadb")
            collections = [c.name for c in client.list_collections()]
            st.sidebar.success(f"Connected! Collections: {', '.join(collections)}")
        except Exception as e:
            st.sidebar.error(f"Connection failed: {e}")

    st.sidebar.header("Portfolio Demo")
    st.sidebar.write("DSR Portfolio Project B42-MHa")
    st.sidebar.write("Cybersecurity RAG System")
    st.sidebar.write("MITRE ATT&CK Integration")


if __name__ == "__main__":
    main()
