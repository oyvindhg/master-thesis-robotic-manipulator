import coordinate_maths

class Position:
    r = 0
    theta = 0
    z = 0
    visible = 1
    def __init__(self, r, theta, z):
        self.r = r
        self.theta = theta
        self.z = z

    def set_invisible(self):
        self.visible = 0

    def set_visible(self):
        self.visible = 1

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

        if pow(x2-x1,2)+pow(y2-y1,2) < length:
            return 1
        return 0

    def distance(self, r, theta, z):
        x1, y1, z1 = coordinate_maths.cartesian(r, theta, z)
        x2, y2, z2 = coordinate_maths.cartesian(self.r, self.theta, self.z)

        return pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2)

obj_pos = {}
obj_num = 0

obj_plan = {}


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

def remove_obj(object_name):
    del obj_pos[object_name]

def objects_match(objects):
    registered_obj = []
    for obj in objects:
        found_obj = 0
        for key in obj_pos:
            if obj_pos[key].is_near(obj.r, obj.theta, obj.z, 5):
                found_obj = 1
                registered_obj.append(key)
        if found_obj == 0:
            return 0
    for key in obj_pos:
        if key not in registered_obj and obj_pos[key].is_visible() == 1:
            return 0
    return 1

def get_invisible():
    obj = []
    for key in obj_pos:
        if not obj_pos[key].is_visible():
            o_pos = {}
            o_pos['name'], num = text_split(key)
            o_pos['r'] = obj_pos[key].r
            o_pos['theta'] = obj_pos[key].theta
            o_pos['z'] = obj_pos[key].z

            obj.append(o_pos)
    return obj

def update_objects(objects):
    obj_pos.clear()
    for obj in objects:
        add_obj(obj)

    o_pos = {}
    for key in obj_pos:
        o_pos['name'], num = text_split(key)
        o_pos['r'] = obj_pos[key].r
        o_pos['theta'] = obj_pos[key].theta
        o_pos['z'] = obj_pos[key].z

    return o_pos

def update_plan_init():

    print("Initial state:")
    for key in obj_pos:
        type, num = text_split(key)

        if type  == "apple" or type == "banana":
            print(key + " - fruit")
        if type == "bowl":
            print(key + " - bowl")

    print("Init:")
    in_bowls = []
    for key in obj_pos:
        type, num = text_split(key)

        r = obj_pos[key].r
        theta = obj_pos[key].theta
        z = obj_pos[key].z

        if type == "bowl":
            first_item = 1
            for key2 in obj_pos:
                type2, num = text_split(key2)
                if key != key2 and (type2 == "apple" or type2 == "banana"):
                    if obj_pos[key2].is_on(r,theta,5):
                        print("in-bowl " + key2 + " " + key)
                        in_bowls.append(key2)
                        if first_item:
                            first_item = 0
                            top = key2
                        else:
                            if obj_pos[key2].z > obj_pos[top].z:
                                print("on " + key2 + " " + top)
                                top = key2
                            else:
                                print("on " + top + " " + key2)
            if not first_item:
                print("on-top " + top)

    for key in obj_pos:
        type, num = text_split(key)
        if type == "apple" or type == "banana":
            if key not in in_bowls:
                print("on-table " + key)

def update_plan_goal():
    print("Goal:")

    key_vec = []
    distance_vec = []

    r = 0
    theta = 0
    z = 0
    for key in obj_pos:
        type, num = text_split(key)
        if type == "bowl":
            r = obj_pos[key].r
            theta = obj_pos[key].theta
            z = obj_pos[key].z

    for key in obj_pos:
        key_vec.append(key)
        distance_vec.append(obj_pos[key].distance(r, theta, z))
    key_vec = [key_vec for _, key_vec in sorted(zip(distance_vec, key_vec))]

    first = 1
    for key in key_vec:
        type, num = text_split(key)
        if type == "banana":
            if first:
                first = 0
            else:
                print("on " + key + " " + last_id)
            last_id = key

    for key in key_vec:
        type, num = text_split(key)
        if type == "apple":
            if first:
                first = 0
            else:
                print("on " + key + " " + last_id)
            last_id = key