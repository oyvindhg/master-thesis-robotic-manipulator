#The restrictions of each joint were added to IKPy.src.ikpy.URDF_utils.py

from IKPy.src import ikpy
import numpy as np
from plan_plot import plot_plan
import math
import logging

logging = logging.getLogger(__name__)

BASE_MODEL = 315
LARM_MODEL = 270
MARM_MODEL = 180
UARM_MODEL = 180
WRIST_MODEL = 180
model = [BASE_MODEL, LARM_MODEL, MARM_MODEL, UARM_MODEL, WRIST_MODEL]

my_chain = ikpy.chain.Chain.from_urdf_file("URDF/dynamixel.URDF")

def joint_to_model_frame(ID, joint_deg):
    model_deg = joint_deg - model[ID]
    return math.radians(model_deg)

def model_to_joint_frame(ID, model_rad):
    model_deg = math.degrees(model_rad)
    joint_deg = model_deg + model[ID]
    logging.debug('Joint %d: %d', ID, joint_deg)
    return joint_deg

def cartesian(r, theta, z):
    x = r*math.cos(math.radians(theta))
    y = r*math.sin(math.radians(theta))
    return [x,y,z]

def rotation_m(x, y, z):

    z = math.radians(z)
    y = math.radians(y)
    x = math.radians(x)

    base_z = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])

    attack_y = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])

    head_x = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])

    rot_matrix = np.dot(np.dot(base_z, attack_y), head_x)

    return rot_matrix


def position_planner(cylinder_target, current_joint_deg, show_plan=False):

    r, theta, z = cylinder_target
    target = cartesian(r, theta, z)

    base_rot = theta
    attack_rot = 90
    head_rot = -60

    rot_matrix = rotation_m(head_rot, attack_rot, base_rot)

    current_model=[0 for i in range(7)]
    for ID, deg in enumerate(current_joint_deg):
        if ID <= 4:
            current_model[ID+1] = joint_to_model_frame(ID, deg)

    target_frame = np.eye(4)

    target_frame[:3, :3] = rot_matrix

    # target_frame[1, 1] = 0.0
    # target_frame[1, 2] = 1.0
    # target_frame[2, 1] = -1.0
    # target_frame[2, 2] = 0.0

    # target_frame[0, 0] = 0.0
    # target_frame[0, 2] = 1.0
    # target_frame[2, 0] = -1.0
    # target_frame[2, 2] = 0.0

    # target_frame[0, 0] = 0.0
    # target_frame[0, 1] = 1.0
    # target_frame[1, 0] = -1.0
    # target_frame[1, 1] = 0.0

    print(current_model)

    target_frame[:3, 3] = target


    print(target_frame)


    model_rad = my_chain.inverse_kinematics(target_frame, initial_position=current_model)

    #plot_plan(my_chain, [0, 0, 0, 0, 0, 0, 0], np.eye(4))

    next_joint_deg = []
    for id, rad in enumerate(model_rad):
        ID = id - 1
        if ID >= 0 and ID <= 4:
            next_joint_deg.append(model_to_joint_frame(ID, rad))

    real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_frame))
    print("Computed position matrix : %s, original position matrix : %s" % (real_frame, target_frame))


    check_sol = next_joint_deg[1] - 180 + next_joint_deg[2] - 180 + next_joint_deg[3] - 180
    if abs(check_sol) > 180:
        logging.warning("The robot is bending through itself")
        plot_plan(my_chain, model_rad, target)
        return False


    logging.info("The angles of each joints in joint ref are: {0}".format(next_joint_deg))
    plot_plan(my_chain, model_rad, target)

    if show_plan:
        logging.info("The angles of each joints in joint ref are: {0}".format(next_joint_deg))
        plot_plan(my_chain, model_rad, target)

    return next_joint_deg

#position_planner([10,0,15], [315, 270, 180, 180, 0, 0, 0], show_plan=True)
#position_planner([10,0,15], [316, 229, 216, 225, 172, 33, 57], show_plan=True)
