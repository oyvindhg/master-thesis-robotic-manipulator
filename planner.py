import pyperplan
import string
import plan_db
import logging
logging = logging.getLogger(__name__)

heuristic = "hff"
search = "astar"
problem = "Planning_tasks/blocks_and_doors/task03.pddl"

def split_text(name):

    for char in string.punctuation:
        name = name.replace(char, ' ')

    return name.split()

def start_plan():
    solution = pyperplan.create_plan(heuristic, search, problem)

    if solution is None:
        logging.warning("No plan was found")
        return None

    for step in solution:
        step_name = step.name
        step.name = split_text(step_name)

    logging.debug(solution)
    return solution


def update_problem(obj_list):
    if not plan_db.objects_match(obj_list):
        extra_obj = plan_db.get_invisible()

        for obj in extra_obj:
            obj_list.append(obj)

        obj_list = plan_db.update_objects(obj_list)

        plan_db.update_plan_init()
        plan_db.update_plan_goal()

obj_list = []

o_pos = {}
o_pos['name'] = 'apple'
o_pos['r'] = 20
o_pos['theta'] = 10
o_pos['z'] = 10

obj_list.append(o_pos)

o_pos = {}
o_pos['name'] = 'apple'
o_pos['r'] = 20
o_pos['theta'] = 10
o_pos['z'] = 8

obj_list.append(o_pos)

o_pos = {}
o_pos['name'] = 'banana'
o_pos['r'] = 20
o_pos['theta'] = 10
o_pos['z'] = 14

obj_list.append(o_pos)

o_pos = {}
o_pos['name'] = 'bowl'
o_pos['r'] = 20
o_pos['theta'] = 10
o_pos['z'] = 5

obj_list.append(o_pos)


update_problem(obj_list)