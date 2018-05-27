import kinect


kinect.init()

# kinect.take_images()

while 1:
    o = kinect.find_objects(show = 1)


print(o)