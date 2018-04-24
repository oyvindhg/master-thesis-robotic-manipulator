import math
import numpy as np

def cartesian(r, theta, z):
    x = r*math.cos(math.radians(theta))
    y = r*math.sin(math.radians(theta))
    return [x,y,z]

def polar(x,y,z):
    r = math.sqrt(math.pow(x,2) + math.pow(y,2))
    theta = math.atan2(y,x)
    theta = math.degrees(theta)
    return [r, theta, z]

def rotation_m(x, y, z):

    z = math.radians(z)
    y = math.radians(y)
    x = math.radians(x)

    base_z = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])

    attack_y = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])

    head_x = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])

    rot_matrix = np.dot(np.dot(base_z, attack_y), head_x)

    return rot_matrix