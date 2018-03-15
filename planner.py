import pyperplan
import string
import world_state

heuristic = "hff"
search = "astar"
problem = "manip_blocktask/task03.pddl"

def split_text(name):

    for char in string.punctuation:
        name = name.replace(char, ' ')

    return name.split()



solution = pyperplan.create_plan(heuristic, search, problem)

op1_name = solution[0].name

op1 = split_text(op1_name)

if op1[0] == "move":
    next_coord = world_state.get_coordinates(op1[2])

    print(next_coord.r, next_coord.theta, next_coord.z)
