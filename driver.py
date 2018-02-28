import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library


# Read present position
def read_current_position(DXL_ID, port_num, PROTOCOL_VERSION, ADDR_PRESENT_POSITION, COMM_SUCCESS):

    position = dynamixel.read2ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_PRESENT_POSITION)
    comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)

    if comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, comm_result))
    elif error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, error))

    return position


# Write goal position
def write_goal_position(DXL_ID, goal, port_num, PROTOCOL_VERSION, ADDR_GOAL_POSITION, COMM_SUCCESS):

    dynamixel.write2ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_GOAL_POSITION, goal)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)

    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

# Enable Dynamixel Torque
def enable_torque(DXL_ID, port_num, PROTOCOL_VERSION, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE, COMM_SUCCESS):
    dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
    else:
        return 1
    return 0

# Set integral
def write_integral(DXL_ID, I, port_num, PROTOCOL_VERSION, ADDR_I, COMM_SUCCESS):

    dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_I, I)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)

    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

# Disable Dynamixel Torque
def disable_torque(DXL_ID, port_num, PROTOCOL_VERSION, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE, COMM_SUCCESS):

    dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)

    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
    elif dxl_error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

# Read current max torque
def read_maximum_torque(DXL_ID, port_num, PROTOCOL_VERSION, ADDR_TORQUE, COMM_SUCCESS):

    torque = dynamixel.read2ByteTxRx(port_num, PROTOCOL_VERSION, DXL_ID, ADDR_TORQUE)
    comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)

    if comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, comm_result))
    elif error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, error))

    return torque

# Close port
def close_port(port_num):

    dynamixel.closePort(port_num)