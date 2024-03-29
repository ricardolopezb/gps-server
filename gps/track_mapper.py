# this creates the list of nodes that is saved in the track mapping class
import cv2

from gps.graph.node import Node


class TrackMapper:
    def define_nodes(self, initial_track_image):
        return self.__get_click_coordinates(initial_track_image)

    def __get_click_coordinates(self, image_path):
        nodes_list = []
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to read the image.")
            return

        image_with_points = image.copy()

        click_counter = 1

        def mouse_callback(event, x, y):
            nonlocal image_with_points, click_counter, nodes_list
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.circle(image_with_points, (x, y), 30, (0, 0, 255), 2)
                cv2.putText(image_with_points, str(click_counter), (x - 5, y + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                cv2.imshow("Image", image_with_points)

                nodes_list.append(Node(click_counter, x, y))
                click_counter += 1

        cv2.imshow("Image", image)

        cv2.setMouseCallback("Image", mouse_callback)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.add_edges(nodes_list)
                cv2.destroyAllWindows()
                break

        self.show_final_nodes_list(nodes_list)
        return nodes_list

    @staticmethod
    def add_edges(nodes_list):
        with open('edges.txt', 'r') as file:
            for line in file:
                line = line.strip()
                from_node_id, to_node_id = line.split('->')
                from_node_id = int(from_node_id.strip())
                to_node_id = int(to_node_id.strip())
                nodes_list[from_node_id - 1].neighbors.append(to_node_id)

    @staticmethod
    def show_final_nodes_list(nodes_list):
        print("Nodes defined successfully.")
        for node in nodes_list:
            print(node.id, node.x, node.y, node.neighbors)
