import kinect


kinect.init()

o = kinect.find_objects(show = 1)


print(o)