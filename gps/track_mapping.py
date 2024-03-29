from collections import deque

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
        return self.get_closest_node(x, y)

    def get_closest_node(self, x, y):
        _, index = self.kd_tree.query([(x, y)])
        closest_index = index[0]
        closest_node = self.nodes[closest_index]
        return closest_node

    def shortest_path(self, start_id, target_id):
        # Initialize a queue for BFS
        queue = deque([(start_id, [start_id])])
        visited = set()  # Set to keep track of visited nodes

        while queue:
            node_id, path = queue.popleft()
            node = next(filter(lambda node: node.id == node_id, self.nodes), None)
            if node_id == target_id:
                return path
            if node_id not in visited:
                visited.add(node_id)
                for neighbor_id in node.neighbors:
                    queue.append((neighbor_id, path + [neighbor_id]))

        # If no path found
        return None
