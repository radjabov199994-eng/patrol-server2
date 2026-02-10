from flask import Flask, request, jsonify

app = Flask(__name__)

last_location = {"lat": 0, "lon": 0}

@app.get("/")
def home():
    return "Patrol server is running", 200

@app.post("/location")
def receive_location():
    data = request.get_json(silent=True) or {}
    try:
        last_location["lat"] = float(data.get("lat", 0))
        last_location["lon"] = float(data.get("lon", 0))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "msg": "lat/lon must be numbers"}), 400
    return jsonify({"status": "ok"})

@app.get("/get_location")
def get_location():
    return jsonify(last_location)

# Render/Gunicorn uchun qo'lda app.run kerak emas
