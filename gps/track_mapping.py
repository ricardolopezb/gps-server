from scipy.spatial import KDTree
from gps.coordinates_provider import CoordinatesProvider


class TrackMapping:
    def __init__(self, nodes):
        self.nodes = nodes
        self.kd_tree = KDTree([(node.x, node.y) for node in nodes])
        self.coordinates_provider = CoordinatesProvider()

    def get_current_car_node(self):
        result = self.coordinates_provider.get_car_coordinates()
        if result is None:
            return None
        x, y = result
        _, index = self.kd_tree.query([(x, y)])
        closest_index = index[0]
        closest_node = self.nodes[closest_index]
        return closest_node