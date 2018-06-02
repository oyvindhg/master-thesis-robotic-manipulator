import motor
import keyboard
import display
import controller
import plan_db
import planner
import sys
import logging
import perception

log_level = "info"
logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(name)-20s %(levelname)-20s %(message)s', stream=sys.stdout)
logging = logging.getLogger(__name__)

# motor.init()
# controller.init()




# controller.close_grippers(wait=0)
#
# import time
# import driver
# while(1):
#     for i in range(5,7):
#         print(driver.alarm_error(i))
# quit()
#
# display.current_status()
#
# controller.init()


# display.current_status()
#
# display.press_key()
# if keyboard.press_ESC():
#     controller.read_only()


# r = 40
# theta = 0
# z = 10
#
# controller.set_position(r, theta, z)
#
# controller.turn_off()
#
# quit()




perception.init()

goal_reached = 0

i = 0

objects = plan_db.get_obj_list()

seen = perception.find_objects(objects, i, show=1)
planner.update_problem(seen, [])

import time

while not goal_reached:

    time.sleep(1)


    plan = planner.make_plan()
    goal_reached = 1

    if plan is None:
        goal_reached = 0
        logging.warning('No plan found!')
    else:
        for step in plan:
            i += 1

            operation = step.action.name
            op_name = operation[0]
            obj = operation[1]

            logging.info('Operation: %s', operation)


            print("press btn")
            keyboard.press_ESC()
            print("next lvl")

            state = step.state

            if op_name == "destack" or op_name == "removelast":

                goal_coord = plan_db.get_coordinates(operation[2])

                obj_upd = {}
                obj_upd['name'] = obj
                obj_upd['r'] = goal_coord.r + 10
                obj_upd['theta'] = goal_coord.theta
                obj_upd['z'] = 0
                obj_upd['visible'] = 1

                planner.update_action(obj_upd)

            if op_name == "stack" or op_name == "insertfirst":

                goal_coord = plan_db.get_coordinates(operation[2])

                obj_upd = {}
                obj_upd['name'] = obj
                obj_upd['r'] = goal_coord.r
                obj_upd['theta'] = goal_coord.theta
                obj_upd['z'] = goal_coord.z + i
                obj_upd['visible'] = operation[2]

                planner.update_action(obj_upd)

            seen = perception.find_objects(objects, i, show=1)
            if planner.update_problem(seen, state):
                goal_reached = 0
                break

logging.info('Reached goal!')


# controller.turn_off()

