from flask import Flask

from gps.track_mapper import TrackMapper
from gps.track_mapping import TrackMapping

# Create a Flask application
app = Flask(__name__)
track_mapping = TrackMapping(TrackMapper().define_nodes("images/image-1.png"))

# Define a route for the home page
@app.route('/')
def home():
    return f"{track_mapping.get_current_car_node()}"

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5200)
