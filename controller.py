import motor
import display
import kinematics
import time

BASE = 0
LARM = 1
MARM = 2
UARM = 3
HEAD = 4
LG = 5
RG = 6

NUM_MOTORS = 7

gripper_midpoint = 45
gripper_closed_distance = 19

safe_height = 30

moving_threshold = 1
torque_threshold = 1

def init():
    motor.activate_all()
    motor.set_I_all(10)
    motor.set_max_vel_arm(40)
    motor.set_rel_goals([0 for ID in range(NUM_MOTORS)])  # Set the goal position of the robot to its current position
    set_head(0)
    set_gripper_torque(20)

def finish_task(show=0):
    while 1:
        if show:
            display.current_pos_status()
        if motor.reached_goal(moving_threshold, torque_threshold):
            return

def gripper(openness, wait=0, show=1):
    motor.set_goal(RG, gripper_midpoint + gripper_closed_distance - openness)
    motor.set_goal(LG, gripper_midpoint - gripper_closed_distance + openness)
    if wait:
        finish_task(show)

def set_gripper_torque(torque):             #torque is % of full torque
    torque = torque*10.23
    torque = int(torque)
    motor.set_max_torque(RG, torque)
    motor.set_max_torque(LG, torque)

def open_grippers(wait=0, show=1):
    gripper(12, wait, show)

def close_grippers(wait=0, show=1):
    gripper(0, wait, show)

def set_head(deg, wait=0, show=1):
    motor.set_goal(HEAD, deg + 180)
    if wait:
        finish_task(show)



def set_position(r, theta, z, wait=1, show=0):

    goal = [r, theta, z]

    current_position = motor.read_positions()
    if show:
        next_position = kinematics.position_planner(goal, current_position, show_plan=True)
    else:
        next_position = kinematics.position_planner(goal, current_position, show_plan=False)

    if next_position is False:
        quit()

    motor.set_goals(next_position)

    if wait:
        finish_task(show)

def go_to(r, theta, z, wait=1, show=0):

    current_joints = motor.read_positions()

    current_pos = kinematics.get_current_position(current_joints)
    height = max(current_pos[2], safe_height)

    set_position(current_pos[0], current_pos[1], height)

    height = max(z, safe_height)
    set_position(r, theta, height)

    set_position(r, theta, z)


def cooldown(location):
    if location == "return":
        motor.set_max_vel_arm(20)
        motor.set_rel_goals(0 for ID in range(NUM_MOTORS))
    else:
        r = 20
        theta = 0
        z = 15
        go_to(r, theta, z, wait=1)
        motor.set_max_vel_arm(20)
        close_grippers(wait=1)
        set_position(r, theta, z-7, wait=1)
    finish_task()

def turn_off(location="absolute"):
    cooldown(location)
    motor.turn_off()

def deactivate_robot():
    motor.activate_all()
    motor.deactivate_all()

def read_only():
    deactivate_robot()
    while 1:
        display.current_status()