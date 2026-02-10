from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Oxirgi joylashuv (default)
last_location = {"lat": 41.3, "lon": 69.2}

# Root - darrov xarita ochilsin (Not Found bo‘lmaydi)
@app.route("/")
def index():
    return render_template("map.html")

# Xarita sahifasi (xohlasang alohida ham ishlaydi)
@app.route("/map")
def map_page():
    return render_template("map.html")

# Location qabul qilish (POST)
@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True) or {}

    # lat/lon kelmasa eski qiymat qoladi
    try:
        last_location["lat"] = float(data.get("lat", last_location["lat"]))
        last_location["lon"] = float(data.get("lon", last_location["lon"]))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "lat/lon number bo‘lishi kerak"}), 400

    return jsonify({"status": "ok", "saved": last_location})

# Location olish (GET)
@app.route("/get_location")
def get_location():
    return jsonify(last_location)

# Version tekshiruv (debug uchun)
@app.route("/version")
def version():
    return "VERSION_2026_02_10_OK"

if __name__ == "__main__":
    # Lokal ishga tushirish uchun (Render gunicorn ishlatadi)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
