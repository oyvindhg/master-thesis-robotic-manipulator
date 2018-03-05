import motor
import keyboard
import display
import controller

#################################################################################
# SETUP:
# Clone Dynamixel SDK into the Pycharm folder.
# Change the dynamixelfunctions.py file in python/dynamixelfunctions.py so that it compiles for Linux 64 bit (or whatever system you use).
# Changed the readwrite.py file in python/protocol1 so that the DynamixelID and baudrate is right.
# Finally, write this in the teminal: "sudo chmod a+rw /dev/ttyUSB0".
# To run: Enter into python/protocol1_0 and run in terminal: "python read_write.py"
#################################################################################

device_name = "/dev/ttyUSB0".encode('utf-8')
motor.init()



NUM_MOTORS = 7
BASE = 0
J1 = 1
J2 = 2
J3 = 3
HEAD = 4
RG = 5
LG = 6

#while 1:
#    position = motor.read_positions()
#    display.current_position()

motor.activate_all()

motor.set_I_all(10)


moving_threshold = 1
position = motor.read_positions()
display.current_position()

rel_goal = [0 for ID in range(NUM_MOTORS)]
motor.set_rel_goals(rel_goal)


i = 0
while 1:
    display.press_key()
    if keyboard.press_ESC():
        break

    i = i + 1

    if i%2 == 0:
        controller.gripper(0)
        #rel_goal[J2] = -2
    else:
        controller.gripper(6)
        #rel_goal[J2] = 2

    #motor.set_rel_goals(rel_goal)

    while 1:

        display.current_status()
        if motor.reached_goal(moving_threshold):
            for elem in rel_goal:
                elem = 0
            break



motor.turn_off()


