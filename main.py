import motor
import keyboard
import display
import controller
import perception
import planner
import sys
import logging

log_level = "info"
logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(name)-20s %(levelname)-20s %(message)s', stream=sys.stdout)
logging = logging.getLogger(__name__)


motor.init()

display.current_status()

controller.init()
display.current_status()

display.press_key()
if keyboard.press_ESC():
    controller.read_only()


controller.set_position(40, 0, 10)

controller.set_position(40, 90, 10)

controller.set_position(40, -30, 10)
quit()

plan = planner.start_plan()

if plan is not None:
    for step in plan:
        operation = step.name
        op_name = operation[0]

        logging.info('Operation: %s', op_name)

        if op_name == "move":
            next_loc_name = operation[2]
            next_loc = perception.get_coordinates(next_loc_name)
            controller.set_position(next_loc.r, next_loc.theta, next_loc.z)

        elif op_name == "pickup":
            controller.open_grippers(wait=1)
            loc_name = operation[2]
            loc = perception.get_coordinates(loc_name)
            controller.set_position(loc.r, loc.theta, loc.z)
            controller.set_position(loc.r, loc.theta, loc.z-10)
            controller.close_grippers(wait=1)
            controller.set_position(loc.r, loc.theta, loc.z)

        elif op_name == "place":
            loc_name = operation[2]
            loc = perception.get_coordinates(loc_name)
            controller.set_position(loc.r, loc.theta, loc.z)
            controller.set_position(loc.r, loc.theta, loc.z-10)
            controller.open_grippers(wait=1)
            controller.set_position(loc.r, loc.theta, loc.z)


controller.turn_off("return")

