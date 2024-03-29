class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
