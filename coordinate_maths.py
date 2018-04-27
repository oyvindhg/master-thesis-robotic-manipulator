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

def rotation_2(b, a, h, x_g, y_g, z_g):

    b = math.radians(b)
    a = math.radians(a)
    h = math.radians(h)
    x_g = math.radians(x_g)
    y_g = math.radians(y_g)
    z_g = math.radians(z_g)

    global_x = np.array([[1, 0, 0], [0, math.cos(x_g), -math.sin(x_g)], [0, math.sin(x_g), math.cos(x_g)]])
    global_z = np.array([[math.cos(z_g), -math.sin(z_g), 0], [math.sin(z_g), math.cos(z_g), 0], [0, 0, 1]])
    global_y = np.array([[math.cos(y_g), 0, math.sin(y_g)], [0, 1, 0], [-math.sin(y_g), 0, math.cos(y_g)]])

    head = np.array([[math.cos(h), -math.sin(h), 0], [math.sin(h), math.cos(h), 0], [0, 0, 1]])
    attack = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
    base = np.array([[1, 0, 0], [0, math.cos(b), -math.sin(b)], [0, math.sin(b), math.cos(b)]])

    rot_matrix = np.dot(np.dot(np.dot(np.dot(np.dot(global_x, global_y), global_z), base), attack), head)

    return rot_matrix
