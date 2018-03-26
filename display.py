import motor

def press_key():
    print("Press any key to continue! (or press ESC to quit!)")

def current_position():
    position = motor.read_positions()
    for i, pos_i in enumerate(position):
        print("[ID:%03d] PresPos: %d" % (i, pos_i))
    print('')

def current_load():
    load = motor.read_loads()
    for i, load_i in enumerate(load):
        print("[ID:%03d] PresLoad: %d" % (i, load_i))
    print('')

def goal_status(ID):
    position = motor.read_positions()
    goal = motor.get_goal()
    print("[ID:%03d] GoalPos: %d  PresPos: %d" % (ID, goal[ID], position[ID]))

def current_pos_status():
    position = motor.read_positions()
    goal = motor.get_goal()
    for ID, _ in enumerate(position):
        print("[ID:%03d] GoalPos: %d  PresPos: %d" % (ID, goal[ID], position[ID]))
    print('')

def current_load_status():
    load = motor.read_loads()
    goal = motor.get_max_torque()
    for ID, _ in enumerate(load):
        print("[ID:%03d] MaxTorque: %d  PresLoad: %d" % (ID, goal[ID], load[ID]))
    print('')

def current_status():
    load = motor.read_loads()
    goal_t = motor.get_max_torque()
    position = motor.read_positions()
    goal = motor.get_goal()
    for ID, _ in enumerate(load):
        print("[ID:%03d] GoalPos: %3d  PresPos: %3d MaxTorque: %3d  PresLoad: %3d" % (ID, goal[ID], position[ID], goal_t[ID], load[ID]))
    print('')