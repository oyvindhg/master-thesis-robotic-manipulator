import motor
import keyboard
import display
import controller
import inv_kinematics

#################################################################################
# SETUP:
# Clone Dynamixel SDK into the Pycharm folder.
# Change the dynamixelfunctions.py file in python/dynamixelfunctions.py so that it compiles for Linux 64 bit (or whatever system you use).
# Changed the readwrite.py file in python/protocol1 so that the DynamixelID and baudrate is right.
# Finally, write this in the teminal: "sudo chmod a+rw /dev/ttyUSB0".
# To run: Enter into python/protocol1_0 and run in terminal: "python read_write.py"
#################################################################################


motor.init()

NUM_MOTORS = 7


display.press_key()
if keyboard.press_ESC():
    controller.read_only()


motor.activate_all()
motor.set_I_all(10)

motor.set_max_vel_arm(40)

motor.set_rel_goals([0 for ID in range(NUM_MOTORS)])       # Set the goal position of the robot to its current position

controller.set_head(0, wait=1)


theta = 90
r = 50
z = 20

controller.gripper(0, wait=1)

controller.set_position(r, theta, z, wait=1)

for i in range(5):
    controller.gripper(6, wait=1)
    controller.gripper(0, wait=1)


print('lol')
controller.set_head(-170)

for i in range(10):
    controller.gripper(6, wait=1)
    controller.gripper(0, wait=1)

controller.set_head(170)

for i in range(30):
    controller.gripper(6)
    controller.gripper(0)

controller.set_head(0, wait=1)

controller.turn_off()

