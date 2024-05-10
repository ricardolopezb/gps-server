from collections import deque

from scipy.spatial import KDTree
from trackmap.coordinates_provider import CoordinatesProvider


class TrackMap:
    def __init__(self, nodes):
        self.nodes = nodes
        self.node_ids = list(nodes.keys())
        self.kd_tree = KDTree([(node.x, node.y) for node in nodes.values()])
        self.coordinates_provider = CoordinatesProvider()

    def get_node(self, node_id):
        return self.nodes[node_id]

    def get_closest_node(self, x, y):
        _, index = self.kd_tree.query([(x, y)])
        closest_index = index[0]
        closest_node_id = self.node_ids[closest_index]
        closest_node = self.nodes[closest_node_id]
        return closest_node

    def get_shortest_path(self, start_id, target_id):
        # Initialize a queue for BFS
        queue = deque([(start_id, [start_id])])
        visited = set()  # Set to keep track of visited nodes

        while queue:
            node_id, path = queue.popleft()
            node = self.nodes.get(node_id)
            if node_id == target_id:
                return path
            if node_id not in visited:
                visited.add(node_id)
                for neighbor in node.neighbors:
                    queue.append((neighbor.id, path + [neighbor.id]))

        # If no path found
        return None
