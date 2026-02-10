from flask import Flask, jsonify

app = Flask(__name__)

# Asosiy sahifa
@app.route("/")
def home():
    return "Patrol server is running ✅"

# Xarita sahifasi (hozircha oddiy)
@app.route("/map")
def map_page():
    return "Map page works ✅"

# Lokatsiya API
@app.route("/get_location")
def get_location():
    return jsonify({
        "lat": 39.6542,
        "lon": 66.9597
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
