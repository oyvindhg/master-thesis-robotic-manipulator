
class Position:
    r = 0
    theta = 0
    z = 0
    def __init__(self, r, theta, z):
        self.r = r
        self.theta = theta
        self.z = z


pos_map = {}

pos_map['l1'] = Position(50, 1, 15)
pos_map['l2'] = Position(30, -30, 25)
pos_map['l3'] = Position(30, 20, 25)


def get_coordinates(location):
    return pos_map[location]