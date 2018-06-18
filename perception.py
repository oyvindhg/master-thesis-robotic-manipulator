import freenect
import numpy as np
import darknet
import os
from show_image import show_labeled
import cv2
from coordinate_maths import polar, rotation_m
from create_3D_model import plot_3d
import statistics
import math
import logging
logging = logging.getLogger(__name__)


DEPTH_REGISTERED   = 4        # processed depth data in mm, aligned to 640x480 RGB
DEPTH_MM           = 5        # depth to each pixel in mm, but left unaligned to RGB image

# cv2.namedWindow('Depth')        #10 bits: Depth is from 0 to 1023. 11th bit gives 2047 if the IR can't read the pattern from the IR projector
# cv2.namedWindow('Image')

depth_y = 480
depth_x = 640

kinect_z = 5
kinect_y = -85
kinect_x = 35
kinect_z_rot = 0
kinect_y_rot = 0
kinect_x_rot = -90


def init():
    darknet.init()
    current_path = os.getcwd()
    darknet_path = current_path + "/darknet"
    config = (darknet_path + "/cfg/yolov3.cfg").encode()
    weights = (darknet_path + "/yolov3.weights").encode()
    metadata = (darknet_path + "/cfg/coco.data").encode()

    global net
    global meta

    net = darknet.load_net(config, weights, 0)
    meta = darknet.load_meta(metadata)

    global kinect_tf

    rot_matrix = rotation_m(kinect_x_rot, kinect_y_rot, kinect_z_rot)
    kinect_tf = np.eye(4)
    kinect_tf[:3, 3] = [kinect_x, kinect_y, kinect_z]
    kinect_tf[:3, :3] = rot_matrix


def pretty_depth(d):

    max = d.max()
    d = d/max * 255
    d = d.astype(np.uint8)

    return d

def show_depth(depth_image):
    depth_copy = np.copy(depth_image)
    depth_im = pretty_depth(depth_copy)
    cv2.imshow('Depth', depth_im)
    return depth_im

def show_image(image):
    cv2.imshow('Image', image)

def get_depth():
    return freenect.sync_get_depth(format=DEPTH_MM)[0]


def get_image():
    im = freenect.sync_get_video()[0]
    return im[:, :, ::-1]

def color_to_depth(image, depth_image):
    return freenect.color_to_depth(image, depth_image)

def isolate_object(image, depth_image, box):
    return freenect.isolate_object(image, depth_image, box)

def depth_to_xyz(depth_image):
    return freenect.depth_to_xy(depth_image)

def object_depth_cm(obj_image, depth_image):

    depth_copy = np.copy(depth_image)

    for y in range(0,depth_y):
        for x in range(0,depth_x):
            if obj_image[y][x][0] == obj_image[y][x][1] == obj_image[y][x][2] == 0:
                depth_copy[y][x] = 0

    xyz = depth_to_xyz(depth_copy)


    x_tot = 0
    y_tot = 0
    z_tot = 0

    x_arr = []
    y_arr = []
    z_arr = []

    i = 0
    for py in range(0,depth_y):
        for px in range(0,depth_x):
            x, y, z = xyz[py][px]

            if x*x + y*y + z*z > 0.0001:
                i += 1
                x_tot += x
                y_tot += y
                z_tot += z

                x_arr.append(x)
                y_arr.append(y)
                z_arr.append(z)

    # x_avg = x_tot/(i* 10 + 1e-10)
    # y_avg = y_tot/(i* 10 + 1e-10)
    # z_avg = z_tot/(i* 10 + 1e-10)
    #
    # print("avg:", x_avg, y_avg, z_avg)

    if x_arr is not []:
        x_med = statistics.median(x_arr) / 10
        y_med = statistics.median(y_arr) / 10
        z_med = statistics.median(z_arr) / 10
    else: x_med = y_med = z_med = 0

    # print("med:", x_med, y_med, z_med)


    return x_med, y_med, z_med

def make_3d():

    # im = get_image()
    waste = get_depth()

    im = np.load("image.npy")
    d = np.load("depth.npy")

    im_d = color_to_depth(im, d)
    xyz = depth_to_xyz(d)

    plot_3d(xyz, im_d)


def take_images():
    im = get_image()
    d = get_depth()
    show_depth(d)
    show_image(im)
    cv2.waitKey()

def find_objects(objects, show = 0, save = 0):


    ############NOOOOOOOOOOOOOOOOOOO

    # obj_list = []
    #
    # o_pos = {}
    # o_pos['name'] = 'apple'
    # o_pos['r'] = 30
    # o_pos['theta'] = 10
    # o_pos['z'] = 10
    # o_pos['visible'] = 1
    #
    # obj_list.append(o_pos)
    # # if i < 2:
    # #     obj_list.append(o_pos)
    #
    # # o_pos = {}
    # # o_pos['name'] = 'banana'
    # # o_pos['r'] = 30
    # # o_pos['theta'] = 10
    # # o_pos['z'] = 10
    # # o_pos['visible'] = 1
    # #
    # # obj_list.append(o_pos)
    # # if i<1:
    # #     obj_list.append(o_pos)
    #
    #
    # o_pos = {}
    # o_pos['name'] = 'bowl'
    # o_pos['r'] = 20
    # o_pos['theta'] = 10
    # o_pos['z'] = 5
    # o_pos['visible'] = 1
    #
    # if i>=3:
    #     o_pos['r'] = 10
    #
    #
    # obj_list.append(o_pos)
    #
    #
    # return obj_list



    ##################################


    im = get_image()
    d = get_depth()


    boxes = darknet.detect(net, meta, im, thresh=0.15)

    logging.debug("Boxes:", boxes)

    if show:
        show_labeled(im, boxes)

    if show:
        show_image(im)
        d_show = show_depth(d)
        cv2.waitKey()
        if save:
            cv2.imwrite("original.png", im)
            cv2.imwrite("depth.png", d_show)
            np.save("image", im)
            np.save("depth", d)
            im_d = color_to_depth(im, d)
            cv2.imwrite("color_to_depth.png", im_d)


    obj = []

    for o in boxes:

        if o[0].decode() not in objects:
            logging.debug(o[0].decode(), "not in objects")
            continue

        im_o = isolate_object(im, d, o)
        if show:
            show_image(im_o)
            cv2.waitKey()
            if save:
                imgname = o[0].decode() + ".png"
                cv2.imwrite(imgname, im_o)

        x, y, z = object_depth_cm(im_o, d)
        if x == y == z == 0:
            logging.debug(o[0].decode(), "at 0 0 0")
            continue

        length = math.sqrt(pow(x,2) + pow(y,2) + pow(z,2))

        # print(o[0], " before :", x, y, z)

        x = x + 3.5 * x / length
        y = y + 3.5 * y / length
        z = z

        # print(o[0], " after :", x, y, z)

        pos = np.array([x, y, z, 1])
        o_world_frame = np.dot(kinect_tf, pos)

        o_polar = polar(o_world_frame[0], o_world_frame[1], o_world_frame[2])

        o_pos = {}
        o_pos['name'] = o[0].decode()
        o_pos['r'] = o_polar[0]
        o_pos['theta'] = o_polar[1]
        o_pos['z'] = o_polar[2]
        o_pos['visible'] = 1
        #
        o_pos['r'] = x
        o_pos['theta'] = y
        o_pos['z'] = z
        o_pos['visible'] = 1
        #


        obj.append(o_pos)


    return obj
