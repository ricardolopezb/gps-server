from flask import Flask

from trackmap.track_map import TrackMap
from trackmap.xml_node_map_reader import XmlNodeMapReader

# Create a Flask application
app = Flask(__name__)
track_mapping = TrackMap(XmlNodeMapReader.read("xml_node_map.xml"))

# Define a route for the home page
@app.route('/')
def home():
    node = track_mapping.get_current_car_node()
    jsonify_node = {
        "id": node.id,
        "x": node.x,
        "y": node.y,
        "neighbors": [neighbor.id for neighbor in node.neighbors]
    }
    return jsonify_node

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5200)
