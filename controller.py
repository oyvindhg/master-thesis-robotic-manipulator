import motor
import display
import inv_kinematics
import math

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

moving_threshold = 1


def finish_task(show=0):
    while 1:
        if show:
            display.current_status()
        if motor.reached_goal(moving_threshold):
            return

def gripper(openness, wait=0, show=1):
    motor.set_goal(RG, gripper_midpoint + gripper_closed_distance - openness)
    motor.set_goal(LG, gripper_midpoint - gripper_closed_distance + openness)
    if wait:
        finish_task(show)

def set_head(deg, wait=0, show=1):
    motor.set_goal(HEAD, deg + 180)
    if wait:
        finish_task(show)

def cartesian(r, theta, z):
    x = r*math.cos(math.radians(theta))
    y = r*math.sin(math.radians(theta))
    return [x,y,z]

def set_position(r, theta, z, wait=0, show=1):

    goal = cartesian(r, theta, z)

    current_position = motor.read_positions()
    next_position = inv_kinematics.position_planner(goal, current_position, show_plan=False)
    motor.set_goals(next_position)

    if next_position == current_position:
        quit()

    if wait:
        finish_task(show)

def cooldown():
    r = 50
    theta = 0
    z = 3
    set_position(r, theta, z, wait=1)
    motor.set_max_vel_arm(20)
    motor.set_rel_goals(0 for ID in range(NUM_MOTORS))
    finish_task()

def turn_off():
    cooldown()
    motor.turn_off()

def deactivate_robot():
    motor.activate_all()
    motor.deactivate_all()

def read_only():
    deactivate_robot()
    while 1:
        display.current_position()