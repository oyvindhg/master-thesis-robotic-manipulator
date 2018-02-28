import motor

def press_key():
    print("Press any key to continue! (or press ESC to quit!)")

def current_position():
    position = motor.read_all()
    for i, pos_i in enumerate(position):
        print("[ID:%03d] PresPos:%03d" % (i, pos_i))
    print('\n')

def goal_status(ID):
    position = motor.read_all()
    goal = motor.get_goal()
    print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (ID, goal[ID], position[ID]))

def full_goal_status():
    position = motor.read_all()
    goal = motor.get_goal()
    for ID, _ in enumerate(position):
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (ID, goal[ID], position[ID]))
    print('\n')