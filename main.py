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

device_name = "/dev/ttyUSB0".encode('utf-8')
motor.init()


NUM_MOTORS = 7


#controller.read_only()

motor.activate_all()
motor.set_I_all(10)
motor.set_max_vel_arm(50)

motor.set_rel_goals([0 for ID in range(NUM_MOTORS)])       # Set the goal position of the robot to its current position

controller.set_head(0)
while 1:
    #display.press_key()
    #if keyboard.press_ESC():
    #    break

    r = 30
    theta = 0
    z = 10

    controller.gripper(0, wait=1)

    controller.set_position(r, theta, z, wait=1)

    controller.gripper(6, wait=1)

    theta = 20

    controller.set_position(r, theta, z, wait=1)



r = 50
theta = 0
z = 10.5
controller.set_position(r, theta, z, wait=1)

motor.turn_off()


