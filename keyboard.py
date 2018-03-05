import sys, tty, termios

ESC_ASCII_VALUE             = 0x1b

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

def press_ESC():
    return get_char() == chr(ESC_ASCII_VALUE)