from flask import Flask, request, jsonify

app = Flask(__name__)

last_location = {"lat": 0, "lon": 0}

@app.route("/")
def home():
    return "Patrol server is running"

@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True) or {}

    last_location["lat"] = float(data.get("lat", 0))
    last_location["lon"] = float(data.get("lon", 0))

    return jsonify({"status": "ok"})

@app.route("/get_location")
def get_location():
    return jsonify(last_location)


# 🔥 MAP SAHIFA
@app.route("/map")
def map_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Patrol Map</title>

        <link rel="stylesheet"
        href="https://unpkg.com/leaflet/dist/leaflet.css" />

        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

        <style>
            html, body, #map {
                height: 100%;
                margin: 0;
            }
        </style>
    </head>

    <body>
        <div id="map"></div>

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
