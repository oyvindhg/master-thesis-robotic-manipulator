import motor
import system
import display
import manager

device_name = "/dev/ttyUSB0".encode('utf-8')
motor.init(device_name)

NUM_MOTORS = 7
BASE = 0
J1 = 1
J2 = 2
J3 = 3
HEAD = 4
RG = 5
LG = 6

motor.activate_all()
moving_threshold = 10
position = motor.read_all()
display.current_position()

rel_goal = [0 for ID in range(NUM_MOTORS)]
motor.set_rel_goals(rel_goal)
motor.change_integral(J3, 10)
motor.change_integral(J2, 10)
motor.change_integral(J1, 10)

i = 0

while 1:
    display.press_key()
    if system.press_ESC():
        break

    i = i + 1

    if i%2 == 0:
        rel_goal[RG] = 60
        rel_goal[LG] = -60
        #rel_goal[J1] = -60
        rel_goal[J2] = -60
    else:
        rel_goal[RG] = -60
        rel_goal[LG] = 60
        #rel_goal[J1] = 60
        rel_goal[J2] = 60

    motor.set_rel_goals(rel_goal)

    while 1:

        display.goal_status(J3)

        if motor.reached_goal(moving_threshold):
            manager.reset(rel_goal)
            break



motor.turn_off()


