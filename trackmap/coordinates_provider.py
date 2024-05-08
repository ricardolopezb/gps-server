# This class takes an image of the track and returns the current coordinates of the car.
import cv2


class CoordinatesProvider:
    def __init__(self):
        self.coordinates = []
        #self.camera = cv.VideoCapture(0). This should be the real camera caputre. For now it's gonna be just the picture
        # self.camera = cv2.imread("images/image-1.png")

    def get_car_coordinates(self):
        # x = self.find_circle_coordinates_with_gui(self.camera)
        return 20, 20
    
        # result = self.__find_circle_coordinates(self.camera)
        # if result is None:
        #     return None
        # x, y = result
        # print(f"Car coordinates: ({x}, {y})")
        # return x, y
    
    # def __find_circle_coordinates(self, image):
    #     # Convert the image to grayscale
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #     # Apply thresholding to segment the black regions
    #     ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    #     # Find contours in the thresholded image
    #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #     # Iterate through contours to find the circle
    #     for contour in contours:
    #         # Approximate the contour to reduce the number of points
    #         epsilon = 0.01 * cv2.arcLength(contour, True)
    #         approx = cv2.approxPolyDP(contour, epsilon, True)
            
    #         # If the contour is circular (approximated to have few points)
    #         if len(approx) > 8:
    #             # Get the center coordinates and radius of the circle
    #             (x, y), radius = cv2.minEnclosingCircle(contour)
    #             center = (int(x), int(y))
                
    #             # Return the coordinates of the circle
    #             return center[0], center[1]
        
    #     # If no circle is found, return None
    #     return None
        
    def find_circle_coordinates_with_gui(self, image):
        # Callback function for the sliders
        def on_trackbar(value):
            nonlocal min_threshold, max_threshold, min_area
            min_threshold = cv2.getTrackbarPos('Min Threshold', 'Parameters')
            max_threshold = cv2.getTrackbarPos('Max Threshold', 'Parameters')
            min_area = cv2.getTrackbarPos('Min Area', 'Parameters')

        # Function to detect circle coordinates with adjustable parameters
        def find_circle_coordinates(image, min_threshold, max_threshold, min_area):
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to segment the black regions
            _, thresh = cv2.threshold(gray, min_threshold, max_threshold, cv2.THRESH_BINARY)

            # Find contours in the thresholded image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Iterate through contours to find the circle
            for contour in contours:
                # Approximate the contour to reduce the number of points
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # If the contour is circular (approximated to have few points) and area is greater than min_area
                if len(approx) > 8 and cv2.contourArea(contour) > min_area:
                    # Get the center coordinates and radius of the circle
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    center = (int(x), int(y))
                    
                    # Return the coordinates of the circle
                    return center[0], center[1]
            
            # If no circle is found, return None
            return None

        # Read the image
        image_copy = image.copy()

        # Create a window and sliders for parameter tuning
        cv2.namedWindow('Parameters')
        cv2.createTrackbar('Min Threshold', 'Parameters', 0, 255, on_trackbar)
        cv2.createTrackbar('Max Threshold', 'Parameters', 0, 255, on_trackbar)
        cv2.createTrackbar('Min Area', 'Parameters', 0, 1000, on_trackbar)

        # Initialize parameters
        min_threshold = 0
        max_threshold = 0
        min_area = 0

        # Main loop
        while True:
            # Detect the circle with current parameters
            circle_coordinates = find_circle_coordinates(image_copy, min_threshold, max_threshold, min_area)
            
            # If circle is found, draw it on the image
            if circle_coordinates is not None:
                circle_x, circle_y = circle_coordinates
                cv2.circle(image_copy, (circle_x, circle_y), 5, (0, 255, 0), -1)
            
            # Display the image
            cv2.imshow('Image', image_copy)
            
            # Check for key press
            key = cv2.waitKey(1)
            if key == ord('r'):  # Press 'r' to return coordinates and quit
                cv2.destroyAllWindows()
                return circle_coordinates