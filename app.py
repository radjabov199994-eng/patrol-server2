from flask import Flask, request, jsonify

app = Flask(__name__)

# Oxirgi joylashuv
last_location = {"lat": 0, "lon": 0}


# Server ishlayaptimi tekshirish
@app.route("/")
def home():
    return "Patrol server is running"


# Location qabul qilish (POST)
@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True) or {}
    last_location["lat"] = float(data.get("lat", 0) or 0)
    last_location["lon"] = float(data.get("lon", 0) or 0)
    return jsonify({"status": "ok"})


# Location olish (GET)
@app.route("/get_location")
def get_location():
    return jsonify(last_location)


# XARITA (GET)
@app.route("/map")
def map_page():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Patrol Map</title>

  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    html, body, #map { height: 100%; margin: 0; padding: 0; }
    .info {
      position: absolute; z-index: 9999; top: 10px; left: 10px;
      background: rgba(0,0,0,0.65); color: #fff; padding: 8px 10px;
      border-radius: 8px; font-family: Arial, sans-serif; font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="info" id="info">Loading...</div>
  <div id="map"></div>

  <script>
    const map = L.map('map').setView([41.3111, 69.2797], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19
    }).addTo(map);

    const marker = L.marker([41.3111, 69.2797]).addTo(map);

    async function refresh() {
      try {
        const r = await fetch('/get_location', { cache: 'no-store' });
        const d = await r.json();

        const lat = Number(d.lat);
        const lon = Number(d.lon);

        document.getElementById('info').textContent =
          `lat: ${lat} | lon: ${lon} | ${new Date().toLocaleTimeString()}`;

        if (lat !== 0 || lon !== 0) {
          marker.setLatLng([lat, lon]);
          map.setView([lat, lon], 16);
        }
      } catch (e) {
        document.getElementById('info').textContent = 'Error: ' + e;
      }
    }

    refresh();
    setInterval(refresh, 3000);
  </script>
</body>
</html>
    """
