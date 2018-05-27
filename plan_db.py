
objects = ['apple1, apple2, banana']

class Position:
    r = 0
    theta = 0
    z = 0
    def __init__(self, r, theta, z):
        self.r = r
        self.theta = theta
        self.z = z

pos_map = {}

pos_map['l1'] = Position(50, 1, 7)
pos_map['l2'] = Position(39.35, -13.22, 2)
pos_map['l3'] = Position(30, 0, 2)


def get_coordinates(location):
    return pos_map[location]