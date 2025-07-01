from src.atp_log_generator import ATPLogGenerator
import json
import requests
import time

g = ATPLogGenerator()
logs = g.generate_attack_sequence("apt29_cozy_bear", 5)

loki_url = "http://10.5.3.3:3100/loki/api/v1/push"
base_time = int(time.time() * 1000000000)

for i, log in enumerate(logs):
    timestamp_ns = str(base_time + i * 1000000000)
    loki_payload = {
        "streams": [
            {
                "stream": {
                    "job": "atp_injection",
                    "level": "info",
                    "source": "atp_generator",
                },
                "values": [[timestamp_ns, json.dumps(log)]],
            }
        ]
    }

    response = requests.post(
        loki_url, json=loki_payload, headers={"Content-Type": "application/json"}
    )
    print(f"Log {i+1}: Status {response.status_code}")
    if response.status_code != 204:
        print(f"Error: {response.text}")
