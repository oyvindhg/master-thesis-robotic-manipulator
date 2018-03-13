#The restrictions of each joint were added to IKPy.src.ikpy.URDF_utils.py

from IKPy.src import ikpy
import numpy as np
import math
from plan_plot import plot_plan


BASE_MODEL = 315
LARM_MODEL = 270
MARM_MODEL = 180
UARM_MODEL = 180
model = [BASE_MODEL, LARM_MODEL, MARM_MODEL, UARM_MODEL]

my_chain = ikpy.chain.Chain.from_urdf_file("URDF/dynamixel.URDF")

def joint_to_model_frame(ID, joint_deg):
    model_deg = joint_deg - model[ID]
    return math.radians(model_deg)

def model_to_joint_frame(ID, model_rad):
    model_deg = math.degrees(model_rad)
    return model_deg + model[ID]

def position_planner(target, current_joint_deg, show_plan=False):

    current_model=[0 for i in range(6)]
    for ID, deg in enumerate(current_joint_deg):
        if ID <= 3:
            current_model[ID+1] = joint_to_model_frame(ID, deg)

    target_frame = np.eye(4)
    target_frame[:3, 3] = target

    model_rad = my_chain.inverse_kinematics(target_frame, initial_position=current_model)

    joint_deg = []
    for id, rad in enumerate(model_rad):
        ID = id - 1
        if ID >= 0 and ID <= 3:
            joint_deg.append(model_to_joint_frame(ID, rad))

    # real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_frame))
    # print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_frame[:3, 3]))

    if show_plan:
        print("The angles of each joints in joint ref are : ", joint_deg)
        plot_plan(my_chain, model_rad, target)

    return joint_deg

#position_planner([10,0,15], [315, 270, 180, 180, 0, 0, 0], show_plan=True)
#position_planner([10,0,15], [316, 229, 216, 225, 172, 33, 57], show_plan=True)
