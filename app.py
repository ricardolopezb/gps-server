from flask import Flask, request

from gps.direction_provider import DirectionProvider
from trackmap.track_map import TrackMap
from trackmap.xml_node_map_reader import XmlNodeMapReader

# Create a Flask application
app = Flask(__name__)
track_mapping = TrackMap(XmlNodeMapReader.read("xml_node_map.xml"))
direction_provider = DirectionProvider(track_mapping)


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


@app.post('/direction')
def direction():
    body = request.get_json()
    direction_provider.set_route(
        (body['start']['x'], body['start']['y']),
        (body['target']['x'], body['target']['y'])
    )
    return direction_provider.get_direction((body['current']['x'], body['current']['y']))



if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5200)
