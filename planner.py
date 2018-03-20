import pyperplan
import string
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
