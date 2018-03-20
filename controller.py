import motor
import display
import inv_kinematics
import math
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
gripper_closed_distance = 18
gripper_closed_distance = 24

moving_threshold = 1
torque_threshold = 1

def init():
    motor.activate_all()
    motor.set_I_all(10)
    motor.set_max_vel_arm(40)
    motor.set_rel_goals([0 for ID in range(NUM_MOTORS)])  # Set the goal position of the robot to its current position

def finish_task(show=0):
    while 1:
        if show:
            display.current_status()
        if motor.reached_goal(moving_threshold, torque_threshold):
            return

def gripper(openness, wait=0, show=1):
    motor.set_goal(RG, gripper_midpoint + gripper_closed_distance - openness)
    motor.set_goal(LG, gripper_midpoint - gripper_closed_distance + openness)
    if wait:
        finish_task(show)

def open_grippers(wait=0, show=1):
    gripper(6, wait, show)

def close_grippers(wait=0, show=1):
    gripper(0, wait, show)

def set_head(deg, wait=0, show=1):
    motor.set_goal(HEAD, deg + 180)
    if wait:
        finish_task(show)

def cartesian(r, theta, z):
    x = r*math.cos(math.radians(theta))
    y = r*math.sin(math.radians(theta))
    return [x,y,z]

def set_position(r, theta, z, wait=1, show=0):

    goal = cartesian(r, theta, z)

    current_position = motor.read_positions()
    if show:
        next_position = inv_kinematics.position_planner(goal, current_position, show_plan=True)
    else:
        next_position = inv_kinematics.position_planner(goal, current_position, show_plan=False)
    motor.set_goals(next_position)

    if next_position == current_position:
        quit()

    if wait:
        finish_task(show)

def cooldown(location):
    if location == "return":
        motor.set_max_vel_arm(20)
        motor.set_rel_goals(0 for ID in range(NUM_MOTORS))
    else:
        r = 50
        theta = 0
        z = 3
        set_head(0)
        set_position(r, theta, z, wait=1)
        motor.set_max_vel_arm(20)
        set_position(r, theta, z-3)
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
        display.current_position()
        display.current_load()
        time.sleep(1)