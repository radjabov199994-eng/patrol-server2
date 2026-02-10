from flask import Flask, request, jsonify

app = Flask(__name__)

last_location = {"lat": 0, "lon": 0}

@app.route("/")
def home():
    return "Patrol server is running"

@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True)

    last_location["lat"] = data.get("lat", 0)
    last_location["lon"] = data.get("lon", 0)

    return jsonify({"status": "ok"})

@app.route("/get_location")
def get_location():
    return jsonify(last_location)
