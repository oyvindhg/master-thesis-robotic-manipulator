import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library
import driver

# Control table address
ADDR_TORQUE_ENABLE       = 24                            # Control table address is different in Dynamixel model
ADDR_GOAL_POSITION       = 30
ADDR_PRESENT_POSITION    = 36
ADDR_BAUDRATE               = 4

# Protocol version
PROTOCOL_VERSION            = 1                             # See which protocol version is used in the Dynamixel

# BAUDRATE                    = 57600
BAUDRATE                    = 1000000

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque

COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed

port = 0
active_motors = []

def activate_motor(ID):
    if ID in active_motors:
        print('Motor already activated')
    elif driver.enable_torque(ID+1, port, PROTOCOL_VERSION, ADDR_TORQUE_ENABLE, TORQUE_ENABLE, COMM_SUCCESS):
        print("Dynamixel motor [ID:%03d] has been successfully connected" % ID)
        active_motors.append(ID)

def activate_several(IDXs):
    for ID in IDXs:
        activate_motor(ID)

def read_position(ID):
    return driver.read_current_position(ID+1, port, PROTOCOL_VERSION, ADDR_PRESENT_POSITION, COMM_SUCCESS)

def read_several(IDXs):
    positions = []
    for ID in IDXs:
        positions.append(read_position(ID))
    return positions

def set_goal(ID, goal):
    if ID in active_motors:
        driver.write_goal_position(ID+1, goal, port, PROTOCOL_VERSION, ADDR_GOAL_POSITION, COMM_SUCCESS)
        return 1
    else:
        print('Motor is not activated')
        return 0

def change_baudrate(ID, baudrate_level):
    # Find baudrate levels in datasheet
    dynamixel.write2ByteTxRx(port, PROTOCOL_VERSION, ID+1, ADDR_BAUDRATE, baudrate_level)

def turn_off():
    for ID in active_motors:
        driver.disable_torque(ID+1, port, PROTOCOL_VERSION, ADDR_TORQUE_ENABLE, TORQUE_DISABLE, COMM_SUCCESS)
    driver.close_port(port)


def init(device_name):
    # Initialize PortHandler Structs
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    port_num = dynamixel.portHandler(device_name)
    # Initialize PacketHandler Structs
    dynamixel.packetHandler()
    # Open port
    if dynamixel.openPort(port_num):
        print("Succeeded to open the port!")
    else:
        print("Failed to open the port!")
        quit()

    # Set port baudrate
    if dynamixel.setBaudRate(port_num, BAUDRATE):
        print("Succeeded to set the baudrate!")
    else:
        print("Failed to change the baudrate!")
        quit()