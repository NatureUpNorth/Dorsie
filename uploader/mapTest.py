#test
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    if request.method == 'POST':
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Here you would save the latitude and longitude to a database
        # For example, using SQLAlchemy:
        # new_location = Location(latitude=latitude, longitude=longitude)
        # db.session.add(new_location)
        # db.session.commit()

        print(f"Received coordinates: Lat={latitude}, Lng={longitude}")
        return jsonify({"message": "Coordinates saved successfully"}), 200
    print("dammit")
    return jsonify({"message": "Invalid request method"}), 405


if __name__ == '__main__':
    app.run(debug=True)
