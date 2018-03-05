import motor

RG = 5
LG = 6

gripper_midpoint = 45
gripper_closed_distance = 18

def gripper(openness):
    motor.set_goal(RG, gripper_midpoint - gripper_closed_distance + openness)
    #motor.set_goal(LG, gripper_midpoint - gripper_closed_distance - openness)