from flask import Flask, request, jsonify

app = Flask(__name__)

last_location = {"lat": 41.3111, "lon": 69.2797}


@app.route("/")
def home():
    return "Patrol server is running"


@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True)

    last_location["lat"] = float(data.get("lat", 0))
    last_location["lon"] = float(data.get("lon", 0))

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

var map = L.map('map').setView([41.3111, 69.2797], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

var marker = L.marker([41.3111, 69.2797]).addTo(map);

async function updateLocation() {

    let res = await fetch('/get_location');
    let data = await res.json();

    marker.setLatLng([data.lat, data.lon]);
    map.setView([data.lat, data.lon], 15);
}

setInterval(updateLocation, 3000);

</script>

</body>
</html>
"""
