import driver

NUM_MOTORS = 7
active_motors = [0 for ID in range(NUM_MOTORS)]
goal_position = [0 for ID in range(NUM_MOTORS)]
initial_position = [0 for ID in range(NUM_MOTORS)]
conv_unit = 0.088

def init():
    driver.init()
    position = read_positions()
    for ID, pos in enumerate(position):
        initial_position[ID] = int(pos)
    print(initial_position)

def unit_to_deg(pos):
    return pos * conv_unit

def deg_to_unit(deg):
    return deg / conv_unit

def change_baudrate(ID, baudrate_level):            # Find baudrate levels in datasheet
    return driver.change_baudrate(ID, baudrate_level)

def activate(ID):                                   # Enable torque
    if active_motors[ID] == 1:
        print('Motor already activated')
        return 0
    else:
        status = driver.activate(ID)
        if status == 1:
            print("Dynamixel motor [ID:%d] has been successfully connected" % ID)
            active_motors[ID] = 1
        return status

def activate_all():
    for ID in (range(NUM_MOTORS)):
        if not activate(ID):
            return 0
    return 1

def deactivate(ID):                                   # Disable torque
    if active_motors[ID] == 0:
        print('Motor already inactive')
        return 0
    else:
        status = driver.deactivate(ID)
        if status == 1:
            active_motors[ID] = 0
            return status

def deactivate_all():
    for ID in (range(NUM_MOTORS)):
        if not deactivate(ID):
            return 0
    return 1

def read_offset(ID):
    return driver.read_offset(ID)

def set_offset(ID, offset):
    return driver.set_offset(ID, offset)

def set_I(ID, I):
    print('Integral for [ID:%d] set to %d' % (ID, I))
    return driver.set_I(ID, I)

def set_I_all(I):
    for ID in (range(NUM_MOTORS)):
        if not set_I(ID, I):
            return 0
    return 1

def read_positions():
    positions = []
    for ID in (range(NUM_MOTORS)):
        pos = driver.read_position(ID)
        pos = unit_to_deg(pos)
        positions.append(pos)
    return positions

def set_goal(ID, goal):                     #DO NOT USE THIS YET UNLESS YOU KNOW WHAT YOU DO
    if active_motors[ID] == 1:
        goal = int(deg_to_unit(goal))
        status = driver.set_goal(ID, goal)
        if status == 1:
            goal_position[ID] = goal
        return status
    else:
        print('Motor is not activated')
        return 0

def get_goal():
    goal_ret = []
    for part_goal in goal_position:
        goal_ret.append(part_goal)
    return goal_ret

def set_rel_goal(ID, delta_pos):
    set_goal(ID, delta_pos + initial_position[ID])
    goal_position[ID] = delta_pos + initial_position[ID]

def set_rel_goals(delta_pos):
    for ID, rel_goal in enumerate(delta_pos):
        set_goal(ID, rel_goal + initial_position[ID])
        goal_position[ID] = rel_goal + initial_position[ID]

def reached_goal(moving_thresh):
    max_dist = 0
    positions = read_positions()
    for ID, pos in enumerate(positions):
        new_dist = abs(pos - goal_position[ID])
        if new_dist > max_dist:
            max_dist = new_dist
    if max_dist < moving_thresh:
        return 1
    return 0


def turn_off():
    for ID in range(NUM_MOTORS):
        deactivate(ID)
    driver.close_port()