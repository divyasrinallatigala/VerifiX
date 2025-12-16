# backend/app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest():
    # Accept JSON with an "extracted" placeholder for now
    payload = request.json or {}
    extracted = payload.get("extracted", {"note":"sample"})
    # Mock response (we replace with Vertex later)
    return jsonify({
        "verification_id": "mock-001",
        "risk_score": 0.1,
        "flags": [],
        "agent_trace": [{"step":"mock","tool":"mock_agent"}],
        "extracted": extracted
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
