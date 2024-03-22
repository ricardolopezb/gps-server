# this creates the list of nodes that is saved in the track mapping class
import cv2

from gps.graph.node import Node


class TrackMapper:
    def define_nodes(self, initial_track_image):
        return self.get_click_coordinates(initial_track_image)

    def get_click_coordinates(self, image_path):
        nodes_list = []
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to read the image.")
            return

        image_with_points = image.copy()

        click_counter = 1

        def mouse_callback(event, x, y, flags, param):
            nonlocal image_with_points, click_counter, nodes_list
            if event == cv2.EVENT_LBUTTONDOWN:
                # Draw a circle at the clicked point with number inside
                cv2.circle(image_with_points, (x, y), 30, (0, 0, 255), 2)
                cv2.putText(image_with_points, str(click_counter), (x - 5, y + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # Display the image with the drawn point
                cv2.imshow("Image", image_with_points)
                # Print the coordinates of the clicked point
                print(f"Clicked at: ({x}, {y})")
                # Increment the click counter
                click_counter += 1
                nodes_list.append(Node(click_counter, x, y))

        # Create a window and display the original image
        cv2.imshow("Image", image)

        # Set the mouse callback function for the window
        cv2.setMouseCallback("Image", mouse_callback)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Close all OpenCV windows
        cv2.destroyAllWindows()
        return nodes_list
