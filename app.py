@app.route("/version")
def version():
    return "VERSION_2026_02_10_01"
from flask import Flask, request, jsonify

app = Flask(__name__)

# Oxirgi joylashuv
last_location = {"lat": 41.3, "lon": 69.2}


@app.route("/")
def home():
    return "Patrol server is running"


# 📍 Location qabul qilish (POST)
@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True) or {}
    last_location["lat"] = float(data.get("lat", 0))
    last_location["lon"] = float(data.get("lon", 0))
    return jsonify({"status": "ok"})


# 📍 Location olish (GET)
@app.route("/get_location")
def get_location():
    return jsonify(last_location)


# 🗺 MAP SAHIFA
@app.route("/map")
def map_page():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Patrol Map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
<style>
  #map { height: 100vh; width: 100%; }
</style>
</head>
<body>

<div id="map"></div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
const map = L.map('map').setView([41.3, 69.2], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);

const marker = L.marker([41.3, 69.2]).addTo(map);

async function refresh() {
  const r = await fetch('/get_location');
  const d = await r.json();
  marker.setLatLng([d.lat, d.lon]);
  map.setView([d.lat, d.lon], 15);
}

setInterval(refresh, 3000);
</script>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
            
