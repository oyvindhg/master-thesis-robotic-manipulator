import perception


perception.init()

# kinect.take_images()

while 1:
    o = perception.find_objects(show = 1)


print(o)