
import cv2
from matplotlib import pyplot as plt
import random

def int_to_color(number):
    """Convert an integer into one of several pre-defined colors."""

    switcher = {
        0: 'crimson',
        1: 'deeppink',
        2: 'dodgerblue',
        3: 'lawngreen',
        4: 'navy',
        5: 'gold',
        6: 'darksalmon',
        7: 'violet',
        8: 'teal',
        9: 'orange'
    }

    return switcher.get(number % len(switcher), "crimson")


def show_labeled(im, boxes):

    if not boxes:
        return

    fig, ax = plt.subplots()
    for box in boxes:  # Iterate through the detected objects

        color = int_to_color(random.randint(0, 9))  # To get some pleasurable graphical variation


        label = box[0].decode("utf-8")
        score = box[1]

        left = round(box[2][0] - 1 / 2 * box[2][2])
        top = round(box[2][1] - 1 / 2 * box[2][3])
        width = round(box[2][2])
        height = round(box[2][3])


        if (left < 0): left = 0
        if (left + width > im.shape[1] - 1): width = im.shape[1] - 1 - left
        if (top < 0): top = 0
        if (top + height > im.shape[0] - 1): height = im.shape[0] - 1 - top

        # Draw rectangle with class name
        ax.add_patch(
            plt.Rectangle((left, top),
                          width,
                          height, fill=False,
                          edgecolor=color, linewidth=3.5, alpha=1)
        )
        ax.text(left, top,
                '{:s}, {:2.1f}%'.format(label, score*100),
                bbox=dict(facecolor=color, alpha=1, edgecolor=color, boxstyle='round'),
                fontsize=14, color='snow')

        # Draw window
    # ax.set_title(('{} detection with '
    #               'p({} | box) >= {:.1f}').format('Object', 'obj',
    #                                               CONF_THRESH),
    #              fontsize=14)
    plt.axis('off')
    plt.tight_layout()


    if ax != None:
        # aximage = ax.imshow(im)
        ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        # aximage.axes.figure.canvas.draw()
        plt.show()