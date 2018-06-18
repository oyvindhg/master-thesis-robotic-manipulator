import pyperplan
import string
import plan_db
import logging
logging = logging.getLogger(__name__)

heuristic = "hff"
search = "astar"
problem = "Planning_tasks/fruits/problem1.pddl"

def split_text(name):

    for char in string.punctuation:
        name = name.replace(char, ' ')

    return name.split()

def make_plan():
    solution = pyperplan.create_plan(heuristic, search, problem)

    if solution is None:
        logging.warning("No plan was found")
        return None


    for step in solution:
        step_name = step.action.name
        step.action.name = split_text(step_name)

    logging.debug(solution)
    return solution


def objects_match(objects, s):

    print(s)

    seen_obj_count = {}
    for obj in objects:
        print(obj)
        if obj['name'] in seen_obj_count:
            seen_obj_count[obj['name']] += 1
        else:
            seen_obj_count[obj['name']] = 1
            print(obj['name'], "regirstered")

    state_obj_count = {}
    bowl_id = []
    for obj in s:
        obj = obj.split()
        if obj[0] == "(ontable":
            obj_name = obj[1].rstrip('0123456789)')
            if obj_name in state_obj_count:
                state_obj_count[obj_name] += 1
            else:
                state_obj_count[obj_name] = 1
                print(obj_name, "also registered")
        if obj[0] == "(empty" and obj[1] not in bowl_id:
            bowl_id.append(obj[1])
            obj_name = obj[1].rstrip('0123456789)')
            if obj_name in state_obj_count:
                state_obj_count[obj_name] += 1
            else:
                state_obj_count[obj_name] = 1
                print(obj_name, "also registered")
        if obj[0] == "(inbowl" and obj[2] not in bowl_id:
            bowl_id.append(obj[2])
            obj_name = obj[2].rstrip('0123456789)')
            if obj_name in state_obj_count:
                state_obj_count[obj_name] += 1
            else:
                state_obj_count[obj_name] = 1
                print(obj_name, "also registered")
    for key in seen_obj_count:
        print(key)
        if not key in state_obj_count:
            print(key, "not found")
            return 0
        else:
            if not seen_obj_count[key] == state_obj_count[key]:
                print(key, "not the same number1: Seen:", seen_obj_count[key], "state:", state_obj_count[key])
                return 0

    for key in state_obj_count:
        if not key in seen_obj_count:
            print(key, "not found")
            return 0
        else:
            if not seen_obj_count[key] == state_obj_count[key]:
                print(key, "not the same number2")
                return 0
    return 1

def update_problem(obj_list, state):
    if not objects_match(obj_list, state):
        logging.info("Replan!")
        plan_db.relocate_objects(obj_list)
        plan_db.write_problem(problem)
        return 1
    plan_db.fix_objects_pos(obj_list)
    return 0

def update_problem_pos(obj_list):
    if not plan_db.objects_match_pos(obj_list):
        logging.info("Replan!")
        plan_db.relocate_objects(obj_list)
        plan_db.write_problem(problem)
        return 1
    return 0

def update_action(obj_upd):
    plan_db.update_object(obj_upd)