from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

last_location = {"lat": None, "lon": None}

@app.route("/")
def home():
    return "Server ishlayapti ✅"

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json(force=True)
    last_location["lat"] = data.get("lat")
    last_location["lon"] = data.get("lon")
    return jsonify({"status": "ok"})

@app.route("/get_location")
def get_location():
    return jsonify(last_location)

@app.route("/map")
def map_view():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
  <title>Patrul xaritasi</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    body, html { margin:0; padding:0; }
    #map { height:100vh; }
  </style>
</head>
<body>
<div id="map"></div>

<script>
  var lat = {{ lat if lat else 41.3111 }};
  var lon = {{ lon if lon else 69.2797 }};

  var map = L.map('map').setView([lat, lon], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(map);

  L.marker([lat, lon]).addTo(map)
    .bindPopup("📍 Patrul shu yerda")
    .openPopup();
</script>
</body>
</html>
""", lat=last_location["lat"], lon=last_location["lon"])

if __name__ == "__main__":
    app.run()
