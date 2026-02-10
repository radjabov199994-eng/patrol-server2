from flask import Flask, request, jsonify

app = Flask(__name__)

# Oxirgi joylashuv saqlanadi
last_location = {"lat": 0, "lon": 0}


# Server ishlayaptimi tekshirish
@app.route("/")
def home():
    return "Patrol server is running"


# Location qabul qilish
@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json(force=True)

    last_location["lat"] = data.get("lat", 0)
    last_location["lon"] = data.get("lon", 0)

    return jsonify({"status": "ok"})


# Location olish
@app.route("/get_location")
def get_location():
    return jsonify(last_location)


# Render uchun MUHIM
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
