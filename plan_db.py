import coordinate_maths
import math

class Position:
    r = 0
    theta = 0
    z = 0
    visible = 1
    def __init__(self, r, theta, z):
        self.r = r
        self.theta = theta
        self.z = z

    def set_visibility(self, visibility):
        self.visible = visibility

    def is_visible(self):
        return self.visible

    def is_near(self, r, theta, z, length):
        x1, y1, z1 = coordinate_maths.cartesian(r, theta, z)
        x2, y2, z2 = coordinate_maths.cartesian(self.r, self.theta, self.z)

        if pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2) < length:
            return 1
        return 0

    def is_on(self, r, theta, length):
        x1, y1, z1 = coordinate_maths.cartesian(r, theta, 0)
        x2, y2, z2 = coordinate_maths.cartesian(self.r, self.theta, 0)

        print(math.sqrt(pow(x2-x1,2)+pow(y2-y1,2)))

        if math.sqrt(pow(x2-x1,2)+pow(y2-y1,2)) < length:
            return 1
        return 0

    def distance(self, r, theta, z):
        x1, y1, z1 = coordinate_maths.cartesian(r, theta, z)
        x2, y2, z2 = coordinate_maths.cartesian(self.r, self.theta, self.z)

        return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2))

obj_pos = {}
obj_num = 0

obj_list = ["apple", "banana", "bowl"]

def get_obj_list():
    return obj_list


def text_split(s):
     head = s.rstrip('0123456789')
     tail = s[len(head):]
     return head, tail

def get_coordinates(object_name):
    return obj_pos[object_name]

def add_obj(object):
    global obj_num
    obj_num += 1
    obj_pos[object['name'] + str(obj_num)] = Position(object['r'], object['theta'], object['z'])
    obj_pos[object['name'] + str(obj_num)].set_visibility(object['visible'])
    print('key:', object['name'] + str(obj_num), 'r:', obj_pos[object['name'] + str(obj_num)].r, 'theta', obj_pos[object['name'] + str(obj_num)].theta, 'z', obj_pos[object['name'] + str(obj_num)].z)

def remove_obj(object_name):

    del obj_pos[object_name]

def fix_objects_pos(obj_list):
    registered_obj = []
    for obj in obj_list:
        print(obj)
        found_obj = 0
        for key in obj_pos:
            print('key:', key, 'r:', obj_pos[key].r, 'theta', obj_pos[key].theta, 'z', obj_pos[key].z)
            type, _ = text_split(key)
            if obj_pos[key].is_near(obj['r'], obj['theta'], obj['z'], 5) and type == obj['name']:
                found_obj = 1
                print("Match!")
                registered_obj.append(key)
        if found_obj == 0:
            return 0

    taken = []
    for key in obj_pos:
        if key not in registered_obj and obj_pos[key].is_visible() == 1:
            type, _ = text_split(key)
            for i, obj in enumerate(obj_list):
                if i not in taken and obj == type:
                    obj_pos[key] = Position(obj['r'], obj['theta'], obj['z'])
                    print("Moved", key, "to", obj['r'], obj['theta'], obj['z'])
                    if obj == "bowl":
                        for key2 in obj_pos:
                            type2, num = text_split(key2)
                            if key != key2 and (type2 == "apple" or type2 == "banana"):
                                if obj_pos[key2].is_on(obj['r'], obj['theta'], 5):
                                    obj_pos[key2] = Position(obj['r'], obj['theta'], obj_pos[key2].z)


def objects_match_pos(objects):
    registered_obj = []
    for obj in objects:
        print(obj)
        found_obj = 0
        for key in obj_pos:
            print('key:', key, 'r:', obj_pos[key].r, 'theta', obj_pos[key].theta, 'z', obj_pos[key].z)
            type, _ = text_split(key)
            if obj_pos[key].is_near(obj['r'], obj['theta'], obj['z'], 5) and type == obj['name']:
                found_obj = 1
                print("Match!")
                registered_obj.append(key)
        if found_obj == 0:
            return 0
    for key in obj_pos:
        if key not in registered_obj and obj_pos[key].is_visible() == 1:
            print(key, " not seen")
            return 0
    return 1

def update_object(object):
    obj_pos[object['name']] = Position(object['r'], object['theta'], object['z'])
    obj_pos[object['name']].set_visibility(object['visible'])

def relocate_objects(objects):
    obj = []
    for key in obj_pos:

        if not obj_pos[key].is_visible():
            o_pos = {}
            o_pos['name'], num = text_split(key)
            o_pos['r'] = obj_pos[key].r
            o_pos['theta'] = obj_pos[key].theta
            o_pos['z'] = obj_pos[key].z
            o_pos['visible'] = 0

            obj.append(o_pos)

    for object in obj:
        print("relocated:", object)
        objects.append(object)

    obj_pos.clear()
    for obj in objects:
        add_obj(obj)

    o_pos = {}
    for key in obj_pos:
        o_pos['name'], num = text_split(key)
        o_pos['r'] = obj_pos[key].r
        o_pos['theta'] = obj_pos[key].theta
        o_pos['z'] = obj_pos[key].z


def write_problem(problem):

    f = open(problem, "w")

    f.write("(define (problem FRUIT-1)\n\n")
    f.write("(:domain FRUIT)\n")
    f.write("\t(:objects\n")

    for key in obj_pos:
        type, num = text_split(key)

        if type  == "apple" or type == "banana":
            f.write("\t\t" + key + " - fruit\n")
        if type == "bowl":
            f.write("\t\t" + key + " - bowl\n")
    f.write("\t)\n\n")


    f.write("\t(:init\n")
    in_bowls = []
    for key in obj_pos:
        type, num = text_split(key)

        r = obj_pos[key].r
        theta = obj_pos[key].theta
        z = obj_pos[key].z


        if type == "bowl":

            in_bowl_id = []
            in_bowl_z = []
            no_item = 1
            for key2 in obj_pos:
                type2, num = text_split(key2)
                if key != key2 and (type2 == "apple" or type2 == "banana"):
                    print("The distance between", key, key2, " is ", obj_pos[key2].is_on(r,theta,5))
                    if obj_pos[key2].is_on(r,theta,5):
                        f.write("\t\t(inbowl " + key2 + " " + key + ")\n")
                        in_bowls.append(key2)
                        in_bowl_id.append(key2)
                        in_bowl_z.append(obj_pos[key2].z)
                        if no_item:
                            no_item = 0

            in_bowl_id = [in_bowl_id for _, in_bowl_id in sorted(zip(in_bowl_z, in_bowl_id))]

            for i, key2 in enumerate(in_bowl_id):
                if i >= 1:
                    f.write("\t\t(on " + key2 + " " + prev + ")\n")
                prev = key2

            if no_item:
                f.write("\t\t(empty " + key + ")\n")
            else:
                f.write("\t\t(ontop " + prev + ")\n")


    for key in obj_pos:
        type, num = text_split(key)
        if type == "apple" or type == "banana":
            if key not in in_bowls:
                f.write("\t\t(ontable " + key + ")\n")
    f.write("\t)\n\n")


    f.write("\t(:goal\n\t\t(and\n")
    key_vec = []
    distance_vec = []

    r = 0
    theta = 0
    z = 0
    bowlkey = 0
    for key in obj_pos:
        type, num = text_split(key)
        if type == "bowl":
            r = obj_pos[key].r
            theta = obj_pos[key].theta
            z = obj_pos[key].z
            bowlkey = key

    if bowlkey is not 0:

        for key2 in obj_pos:
            key_vec.append(key2)
            distance_vec.append(obj_pos[key2].distance(r, theta, z))
        key_vec = [key_vec for _, key_vec in sorted(zip(distance_vec, key_vec))]

        first = 1
        for key2 in key_vec:
            type, num = text_split(key2)
            if type == "banana":
                f.write("\t\t(inbowl " + key2 + " " + bowlkey + ")\n")
                if first:
                    first = 0
                else:
                    f.write("\t\t(on " + key2 + " " + last_id + ")\n")
                last_id = key2

        for key2 in key_vec:
            type, num = text_split(key2)
            if type == "apple":
                f.write("\t\t(inbowl " + key2 + " " + bowlkey + ")\n")
                if first:
                    first = 0
                else:
                    f.write("\t\t(on " + key2 + " " + last_id + ")\n")
                last_id = key2
        f.write("\t\t)\n\t)\n)")

    f.close()