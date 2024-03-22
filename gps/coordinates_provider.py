# This class takes an image of the track and returns the current coordinates of the car.
import cv2 as cv


class CoordinatesProvider:
    def __init__(self):
        self.coordinates = []
        self.camera = cv.VideoCapture(0)

    def get_car_coordinates(self):
        return self.coordinates