import motor
import system
import dynamixel_functions as dynamixel

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


position = [0 for ID in range(NUM_MOTORS)]
goal_position = [[0 for idx in range(2)] for ID in range(NUM_MOTORS)]
index = 0


# while(1):
#     read_positions = motor.read_several(range(NUM_MOTORS))
#     for pos in range(NUM_MOTORS):
#         print("[ID:%03d] PresPos:%03d" % (pos, read_positions[pos]))
#     print('\n')


motor.activate_several(range(NUM_MOTORS))

moving_threshold = 10


position[RG] = motor.read_position(RG)
goal_position[RG] = [position[RG] - 20, position[RG] + 20]

position[LG] = motor.read_position(LG)
goal_position[LG] = [position[LG] + 20, position[LG] - 20]

position = motor.read_several(range(NUM_MOTORS))
for pos in range(NUM_MOTORS):
    print("[ID:%03d] PresPos:%03d" % (pos, position[pos]))

# print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (RG, goal_position[RG][index], position[RG]))
# print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (LG, goal_position[LG][index], position[LG]))


while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if system.press_ESC():
        break

    # if not motor.set_goal(RG, goal_position[RG][index]):
    #     break
    #
    # if not motor.set_goal(LG, goal_position[LG][index]):
    #     break

    J3g = position[J3] + 20
    if not motor.set_goal(J3, J3g):
        break

    while 1:

        position[J3] = motor.read_position(J3)
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (J3, J3g, position[J3]))

        if not (abs(J3g - position[J3]) > moving_threshold):
            break

        # position[RG] = motor.read_position(RG)
        # print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (RG, goal_position[RG][index], position[RG]))
        #
        # position[LG] = motor.read_position(LG)
        # print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (LG, goal_position[LG][index], position[LG]))
        #
        # if not (abs(goal_position[RG][index] - position[RG]) > moving_threshold):
        #     break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0


motor.turn_off()


