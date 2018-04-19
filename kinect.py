import freenect
from libfreenect.wrappers.python import frame_convert2
import numpy as np
#import darknet.run_python as dn
import os, time
from show_image import show_labeled
import cv2
from create_3D_model import plot_3d


DEPTH_REGISTERED   = 4        # processed depth data in mm, aligned to 640x480 RGB
DEPTH_MM           = 5        # depth to each pixel in mm, but left unaligned to RGB image

# cv2.namedWindow('Depth')        #10 bits: Depth is from 0 to 1023. 11th bit gives 2047 if the IR can't read the pattern from the IR projector
# cv2.namedWindow('Image')

depth_y = 480
depth_x = 640

def show_depth(depth_image):
    depth_im = frame_convert2.pretty_depth_cv(depth_image)
    cv2.imshow('Depth', depth_im)

def show_image(image):
    cv2.imshow('Image', image)

def get_depth():
    return freenect.sync_get_depth(format=DEPTH_MM)[0]

def get_image():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

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
    i = 0
    for py in range(0,depth_y):
        for px in range(0,depth_x):
            x, y, z = xyz[py][px]
            if x*x + y*y + z*z > 0.0001:
                i += 1
                x_tot += x
                y_tot += y
                z_tot += z

    x_avg = x_tot/(i * 10)
    y_avg = y_tot/(i * 10)
    z_avg = z_tot/(i * 10)

    return x_avg, y_avg, z_avg





im = get_image()
d = get_depth()
#
show_image(im)
show_depth(d)
cv2.waitKey()

# np.save("image", im)
# np.save("depth", d)

# im = np.load("image.npy")
# waste = get_depth()
# d = np.load("depth.npy")


# main_path = os.getcwd()
# net_path = main_path + '/darknet'
# os.chdir(net_path)
#
# method = "yolo"
#
# if method == "yolo9000":
#     config = b"cfg/yolo9000.cfg"
#     weights = b"yolo9000.weights"
#     metadata = b"cfg/combine9k.data"
# else:
#     config = b"cfg/yolo.cfg"
#     weights = b"yolo.weights"
#     metadata = b"cfg/coco.data"
#
# dn.init(net_path)
# net = dn.load_net(config, weights, 0)
# meta = dn.load_meta(metadata)
# boxes = dn.detection2(net, meta, im, thresh=0.1)
#
# print(boxes)
#
# show_labeled(im, boxes)
# for obj in boxes:
#
#     im2 = isolate_object(im, d, obj)
#     show_image(im2)
#     cv2.waitKey()
#
#     x, y, z = object_depth_cm(im2, d)
#     print("Pos:", x, y, z)



#print("ok")
#
# #print(m)
#
# m = np.zeros((2,3,3))
# # #
# m[0][1][0] = 5
# m[1][1][0] = 2.5
# m[0][0][2] = 5
# m[0][2][1] = 2.5
#


#
#
#
quit()

cont = True
while cont:
    a = get_depth()
    im = get_image()


    same = color_to_depth(im, a)



    show_depth(a)
    show_image(same)



    # main_path = os.getcwd()
    # net_path = main_path + '/darknet'
    # os.chdir(net_path)
    #
    # method = "yolo"
    #
    # if method == "yolo9000":
    #     config = b"cfg/yolo9000.cfg"
    #     weights = b"yolo9000.weights"
    #     metadata = b"cfg/combine9k.data"
    # else:
    #     config = b"cfg/yolo.cfg"
    #     weights = b"yolo.weights"
    #     metadata = b"cfg/coco.data"
    #
    # dn.init(net_path)
    # net = dn.load_net(config, weights, 0)
    # meta = dn.load_meta(metadata)
    # boxes = dn.detection2(net, meta, im)
    # print('boxes:', boxes)

    # boxes = [(b'bicycle', 0.8509225845336914, (341.80010986328125, 285.9195861816406, 493.32745361328125, 324.6991882324219))]

    #show_labeled(im, boxes)

    #idea: extend registration.c/freenect_map_rgb_to_depth so that it takes left top and bottom right corner of BBs and finds new BBs


    if cv2.waitKey(10) == 27:
        break