import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library


# Read present position
def getPosition(port, ID, PROTOCOL_VERSION = 1, ADDR_PRESENT_POSITION = 36, COMM_SUCCESS = 0):

    position = dynamixel.read2ByteTxRx(port, PROTOCOL_VERSION, ID, ADDR_PRESENT_POSITION)
    comm_result = dynamixel.getLastTxRxResult(port, PROTOCOL_VERSION)
    error = dynamixel.getLastRxPacketError(port, PROTOCOL_VERSION)

    if comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, comm_result))
    elif error != 0:
        print(dynamixel.getRxPacketError(PROTOCOL_VERSION, error))

    return position