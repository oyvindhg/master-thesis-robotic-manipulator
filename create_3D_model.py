import pandas as pd
from pyntcloud.pyntcloud import PyntCloud
import numpy as np

NUMPOINTS = 100

def setcolor(color_name="specify"):
    if color_name == "green":
        return np.array([0, 0, 255]).astype(np.uint8)
    elif color_name == "blue":
        return np.array([0, 255, 0]).astype(np.uint8)
    elif color_name == "red":
        return np.array([255, 0, 0]).astype(np.uint8)
    elif color_name == "white":
        return np.array([255, 255, 255]).astype(np.uint8)
    else:
        return (np.random.uniform(size=(1, 3)) * 255).astype(np.uint8)

def reshape_to_3d_arr(xyz_arr):
    arr_3d = np.reshape(xyz_arr, (-1, 3))
    return arr_3d

def scale_to_unit(xyz_arr):
    max_num = float(abs(xyz_arr).max())


    return xyz_arr / max_num

def plot_3d(xyz_arr, rgb_im, filename = "room.ply"):


    positions = scale_to_unit(reshape_to_3d_arr(xyz_arr))


    #positions = np.random.uniform(size=(NUMPOINTS, 3)) - 50

    #print(positions)

    points = pd.DataFrame(positions, columns=['x', 'y', 'z'])

    colors = np.zeros((int(positions.size / 3),3))
    for i in range(0,int(positions.size / 3)):
        colors[i][:] = setcolor('white')
        if positions[i][2] == 0:
            colors[i][:] = setcolor('green')

    rgb_3d = reshape_to_3d_arr(rgb_im)


    for i in range(0, int(positions.size / 3)):
        colors[i][:] = np.array([rgb_3d[i][2], rgb_3d[i][0], rgb_3d[i][1]]).astype(np.uint8)
    #
    # for i in range(0, int(positions.size / 3)):
    #     if i < positions.size / 6:
    #         colors[i][:] = setcolor('green')
    #     else:
    #         colors[i][:] = setcolor('red')


    points[['red', 'blue', 'green']] = pd.DataFrame(colors, index=points.index)


    cloud = PyntCloud(points)
    cloud.to_file(filename)