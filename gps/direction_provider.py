class DirectionProvider:
    def __init__(self, map):
        self.map = map
        self.previous_node = None
        self.path = None

    def set_route(self, start_coordinates, target_coordinates):
        start_node = self.map.get_closest_node(*start_coordinates)
        target_node = self.map.get_closest_node(*target_coordinates)

        print(f"GOING FROM Node-{start_node.id} TO Node-{target_node.id}")

        # Maybe change the method params for the coordinates directly
        path = self.map.get_shortest_path(start_node.id, target_node.id)
        self.path = path

    def get_direction(self, current_position, is_blind=False):
        current_node = self.map.get_closest_node(*current_position)
        if not current_node.is_critical and not is_blind:
            self.previous_node = current_node
            return {'status': 'unmodified', 'steer': 0}
        current_node_index = self.path.index(current_node)
        if current_node_index + 1 == len(self.path):
            return {'status': 'reached destination', 'steer': 0}
        next_node = self.path[current_node_index + 1]

        trajectory_vector = self._get_trajectory_vector(current_node)
        route_vector = self._get_route_vector(current_node, next_node)
        correction_vector = self._get_correction_vector(trajectory_vector, route_vector)
        correction_vector_length = (correction_vector[0] ** 2 + correction_vector[1] ** 2) ** 0.5
        angle = self._calculate_steering_angle(correction_vector, correction_vector_length)
        return {'status': 'steering', 'steer': angle}


    def _get_route_vector(self, current_node, next_node):
        return next_node.x - current_node.x, next_node.y - current_node.y

    def _get_trajectory_vector(self, current_node):
        return current_node.x - self.previous_node.x, current_node.y - self.previous_node.y

    def _get_correction_vector(self, trajectory_vector, route_vector):
        return trajectory_vector - route_vector

    def _calculate_steering_angle(self, correction_vector, correction_vector_length):
        print("Vector: ", correction_vector)
        print("Length: ", correction_vector_length)
        return 0
        # if correction_vector_length == 0:
        #     return 0
        # if correction_vector_length < 0.1:
        #     return 0
        # if 0.1 <= correction_vector[0] < 0.5:
        #     return 12
        # if 0.5 <= correction_vector[0] < 1:
        #     return 22

