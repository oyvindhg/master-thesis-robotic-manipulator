import motor

def press_key():
    print("Press any key to continue! (or press ESC to quit!)")

def current_position():
    position = motor.read_positions()
    for i, pos_i in enumerate(position):
        print("[ID:%03d] PresPos: %d" % (i, pos_i))

def goal_status(ID):
    position = motor.read_positions()
    goal = motor.get_goal()
    print("[ID:%03d] GoalPos: %d  PresPos: %d" % (ID, goal[ID], position[ID]))

def current_status():
    position = motor.read_positions()
    goal = motor.get_goal()
    for ID, _ in enumerate(position):
        print("[ID:%03d] GoalPos: %d  PresPos: %d" % (ID, goal[ID], position[ID]))