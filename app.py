from flask import Flask

from gps.track_mapper import TrackMapper
from gps.track_mapping import TrackMapping

# Create a Flask application
app = Flask(__name__)
track_mapping = TrackMapping(TrackMapper().define_nodes())

# Define a route for the home page
@app.route('/')
def home():
    return 'Hello, World! This is a simple Flask app.'

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5200)
