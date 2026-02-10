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

@app.route("/map")
def map_page():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Patrol Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<style>
html, body, #map { height: 100%; margin: 0; }
</style>
</head>
<body>
<div id="map"></div>
<script>
const map = L.map('map').setView([41.3111, 69.2797], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

const marker = L.marker([0,0]).addTo(map);

async function refresh(){
    const r = await fetch('/get_location');
    const d = await r.json();
    if(d.lat !== 0 && d.lon !== 0){
        marker.setLatLng([d.lat, d.lon]);
        map.setView([d.lat, d.lon], 16);
    }
}

refresh();
setInterval(refresh, 3000);
</script>
</body>
</html>
"""
