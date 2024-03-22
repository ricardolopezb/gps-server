# this creates the list of nodes that is saved in the track mapping class
import cv2


class TrackMapper:
    def define_nodes(self, initial_track_image):
        pass

    def get_click_coordinates(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Unable to read the image.")
            return

        # Create a copy of the image for displaying clicked points
        image_with_points = image.copy()

        # Create a callback function to handle mouse events
        def mouse_callback(event, x, y, flags, param):
            nonlocal image_with_points
            if event == cv2.EVENT_LBUTTONDOWN:
                # Draw a circle at the clicked point
                cv2.circle(image_with_points, (x, y), 5, (0, 0, 255), -1)
                # Display the image with the drawn point
                cv2.imshow("Image", image_with_points)
                # Print the coordinates of the clicked point
                print(f"Clicked at: ({x}, {y})")

        # Create a window and display the original image
        cv2.imshow("Image", image)

        # Set the mouse callback function for the window
        cv2.setMouseCallback("Image", mouse_callback)

        # Wait for the user to click on the image
        cv2.waitKey(0)

        # Close all OpenCV windows
        cv2.destroyAllWindows()