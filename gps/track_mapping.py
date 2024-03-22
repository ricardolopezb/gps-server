from gps.coordinates_provider import CoordinatesProvider


class TrackMapping:
    def __init__(self, nodes):
        self.nodes = nodes
        self.coordinates_provider = CoordinatesProvider()

    def get_current_car_node(self):
        return self.nodes[0]