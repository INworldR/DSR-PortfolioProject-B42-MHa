#\!/bin/bash
# DSR Portfolio Project - Service Startup Script
# Auto-start services after container reboot

set -e

LOG_FILE="/tmp/service_startup.log"
exec > >(tee -a "") 2>&1

echo "[Tue Jul  1 11:00:29 CEST 2025] Starting DSR Portfolio Project services..."

# Change to project directory
cd /workspace/DSR-PortfolioProject-B42-MHa

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "[Tue Jul  1 11:00:29 CEST 2025] Activating virtual environment..."
    source .venv/bin/activate
fi

# Install/update requirements
echo "[Tue Jul  1 11:00:29 CEST 2025] Checking Python requirements..."
pip install -q -r requirements.txt

# Start Streamlit ATP Demo
echo "[Tue Jul  1 11:00:29 CEST 2025] Starting Streamlit ATP Demo on port 8501..."
nohup streamlit run src/streamlit_atp_demo.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > /tmp/streamlit.log 2>&1 &
STREAMLIT_PID=$\!

# Wait for Streamlit to start
sleep 5

# Check if services are running
echo "[Tue Jul  1 11:00:29 CEST 2025] Checking service status..."
if curl -s http://localhost:8501 > /dev/null; then
    echo "[Tue Jul  1 11:00:29 CEST 2025] Streamlit ATP Demo running on port 8501"
else
    echo "[Tue Jul  1 11:00:29 CEST 2025] Streamlit failed to start"
fi

echo "[Tue Jul  1 11:00:29 CEST 2025] Service startup complete. PIDs: Streamlit=$STREAMLIT_PID"
echo "[Tue Jul  1 11:00:29 CEST 2025] Logs: Streamlit=/tmp/streamlit.log, Startup=/tmp/service_startup.log"

# Keep script running to maintain services
wait
