import driver
import logging
logging = logging.getLogger(__name__)

NUM_MOTORS = 7
active_motors = [0 for ID in range(NUM_MOTORS)]
goal_position = [0 for ID in range(NUM_MOTORS)]
goal_torque = [0 for ID in range(NUM_MOTORS)]
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
        logging.info('Motor already activated')
        return 0
    else:
        status = driver.activate(ID)
        if status == 1:
            logging.info("Dynamixel motor [ID:%d] has been successfully connected", ID)
            active_motors[ID] = 1
        return status

def activate_all():
    for ID in (range(NUM_MOTORS)):
        if not activate(ID):
            return 0
    return 1

def deactivate(ID):                                   # Disable torque
    if active_motors[ID] == 0:
        logging.info('Motor already inactive')
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

def read_CCW_limit(ID):
    return driver.read_CCW_limit(ID)

def set_CCW_limit(ID, ccw):
    logging.info('CCW limit for [ID:%d] set to %d', ID, ccw)
    return driver.set_CCW_limit(ID, ccw)

def read_CW_limit(ID):
    return driver.read_CW_limit(ID)

def set_CW_limit(ID, cw):
    logging.info('CW limit for [ID:%d] set to %d', ID, cw)
    return driver.set_CW_limit(ID, cw)

def set_mode(ID, mode):
    if mode == "wheel":
        set_CW_limit(ID, 0)
        set_CCW_limit(ID, 0)
    elif mode == "joint":
        set_CW_limit(ID, 0)
        if ID == 0:
            set_CCW_limit(ID, 4095)                      #Default 4095 for BASE
        elif ID == 5 or 6:
            set_CCW_limit(ID, 1023)                      #Default 1023 for LG and RG

def set_I(ID, I):
    logging.info('Integral for [ID:%d] set to %d', ID, I)
    return driver.set_I(ID, I)

def set_I_all(I):
    for ID in (range(NUM_MOTORS)):
        if not set_I(ID, I):
            return 0
    return 1

def set_max_vel(ID, max_vel):
    logging.info('Max velocity of [ID:%d] set to %d RPM', ID, max_vel*0.114)
    return driver.set_max_vel(ID, max_vel)

def set_max_vel_arm(max_vel):
    for ID in (range(NUM_MOTORS)):
        if ID <= 3:
            if not set_max_vel(ID, max_vel):
                return 0
    return 1

def read_positions():
    positions = []
    for ID in (range(7)):
        pos = driver.read_position(ID)
        if pos == None:
            logging.info("fault in motor %d, could not read!", ID)
        if pos > 32767:
            pos = (65535 - pos) * (-1)      #Converting two bytes from unsigned to signed
        pos = unit_to_deg(pos)
        positions.append(pos)
    return positions

def read_loads():
    loads = []
    for ID in (range(7)):
        load = driver.read_load(ID)
        if load == None:
            logging.info("fault in motor %d, could not read!", ID)
        elif load >= 1024:
            load = load - 1024
        loads.append(load)
    return loads

def set_goal(ID, goal):
    if active_motors[ID] == 1:
        unit_goal = int(deg_to_unit(goal))
        status = driver.set_goal(ID, unit_goal)
        if status == 1:
            goal_position[ID] = goal
        return status
    else:
        logging.warning('Motor %d is not activated', ID)
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

def reached_goal(moving_thresh, torque_thresh):

    positions = read_positions()
    torques = read_loads()
    for ID, pos in enumerate(positions):

        torque_ok = 0

        if goal_torque[ID] is not 0:
            new_torque_dist = abs(torques[ID] - goal_torque[ID])
            logging.debug("Torque difference on ID %d: %d", ID, new_torque_dist)
            if new_torque_dist <= torque_thresh:
                torque_ok = 1

        new_dist = abs(pos - goal_position[ID])
        logging.debug("Distance difference on ID %d: %d", ID, new_dist)
        if new_dist > moving_thresh and not torque_ok:
            return 0
    return 1

def read_max_torque(ID):
    return driver.read_max_torque(ID)

def set_max_torque(ID, torque):
    if active_motors[ID] == 1:
        logging.info('Torque limit for [ID:%d] set to %d', ID, torque)
        status = driver.set_max_torque(ID, torque)
        if status == 1:
            goal_torque[ID] = torque
        return status
    else:
        logging.warning('Motor %d is not activated', ID)
        return 0

def get_max_torque():
    torque_ret = []
    for part_t in goal_torque:
        torque_ret.append(part_t)
    return torque_ret

def turn_off():
    for ID in range(NUM_MOTORS):
        deactivate(ID)
    driver.close_port()



# def enable_torque_mode(ID):
#     logging.info('Enabled torque mode')
#     return driver.enable_torque_mode(ID)
#
# def disable_torque_mode(ID):
#     logging.info('Disabled torque mode')
#     return driver.disable_torque_mode(ID)
#
# def set_goal_torque(ID, dir, torque):
#     if active_motors[ID] == 1:
#         if dir == "CCW":
#             status = driver.set_goal_torque(ID, torque)
#         else:
#             status = driver.set_goal_torque(ID, torque + 1024)
#         if status == 1:
#             goal_torque[ID] = torque
#         return status
#     else:
#         logging.warning('Motor %d is not activated', ID)
#         return 0
#
# def get_torque_goal():
#     torque_ret = []
#     for part_t in goal_torque:
#         torque_ret.append(part_t)
#     return torque_ret
#
# def reached_torque(ID, torque_thresh):
#     loads = read_loads()
#     dist = abs(loads[ID] - goal_torque[ID])
#     if dist < torque_thresh:
#         return 1
#     return 0