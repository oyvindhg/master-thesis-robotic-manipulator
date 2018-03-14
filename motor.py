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

def read_CCW_limit(ID):                     #Default 4095 for BASE
    return driver.read_CCW_limit(ID)

def set_CCW_limit(ID, ccw):
    print('CCW limit for [ID:%d] set to %d' % (ID, ccw))
    return driver.set_CCW_limit(ID, ccw)

def read_CW_limit(ID):                     #Default 0 for BASE
    return driver.read_CW_limit(ID)

def set_CW_limit(ID, cw):
    print('CW limit for [ID:%d] set to %d' % (ID, cw))
    return driver.set_CW_limit(ID, cw)

def set_I(ID, I):
    print('Integral for [ID:%d] set to %d' % (ID, I))
    return driver.set_I(ID, I)

def set_I_all(I):
    for ID in (range(NUM_MOTORS)):
        if not set_I(ID, I):
            return 0
    return 1

def set_max_vel(ID, max_vel):
    print('Max velocity of [ID:%d] set to %d RPM' % (ID, max_vel*0.114))
    return driver.set_max_vel(ID, max_vel)

def set_max_vel_arm(max_vel):
    for ID in (range(NUM_MOTORS)):
        if ID <= 3:
            if not set_max_vel(ID, max_vel):
                return 0
    return 1

def read_positions():
    positions = []
    for ID in (range(NUM_MOTORS)):
        pos = driver.read_position(ID)
        if pos > 32767:
            pos = (65535 - pos) * (-1)      #Converting two bytes from unsigned to signed
        pos = unit_to_deg(pos)
        positions.append(pos)
    return positions

def set_goal(ID, goal):                     #DO NOT USE THIS YET UNLESS YOU KNOW WHAT YOU DO
    if active_motors[ID] == 1:
        unit_goal = int(deg_to_unit(goal))
        status = driver.set_goal(ID, unit_goal)
        if status == 1:
            goal_position[ID] = goal
        return status
    else:
        print('Motor is not activated')
        return 0

def set_goals(goals):
    for ID, goal in enumerate(goals):
        set_goal(ID, goal)


def get_goal():
    goal_ret = []
    for part_goal in goal_position:
        goal_ret.append(part_goal)
    return goal_ret

def set_rel_goal(ID, delta_pos):
    set_goal(ID, delta_pos + initial_position[ID])
    #goal_position[ID] = delta_pos + initial_position[ID]

def set_rel_goals(delta_pos):
    for ID, rel_goal in enumerate(delta_pos):
        set_goal(ID, rel_goal + initial_position[ID])
        #goal_position[ID] = rel_goal + initial_position[ID]

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