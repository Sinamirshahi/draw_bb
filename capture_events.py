# import the necessary packages
import cv2
import argparse
import json
from pathlib import Path
import os

# now let's initialize the list of reference point
ref_point = []
bounding_box = []
list = []
json_list = ''
layout_output_file = ''
invoice_height = 800 # window max height for large invoices
i = 0

def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, bounding_box, crop

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        bounding_box = [(x, y)]
        #print(bounding_box)

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))
        width = x - ref_point[0][0]
        #print (width)
        height = y - ref_point[0][1]
        #print (height)
        bounding_box.append((width, height))
        print (bounding_box)

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)
        list.append(bounding_box)
        #list.append(ref_point)
        # print(list)
        json_list = json.dumps(list)
        # print(json_list)
        print(json_list, file=open(layout_output_file, 'w'))


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
    
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

filename_w_ext = os.path.basename(args["image"])
filename, file_extension = os.path.splitext(filename_w_ext)
layout_output_file = f'layouts/layout_{filename}.json'

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)


# keep looping until the 'q' key is pressed
while True:
    image = ResizeWithAspectRatio(image, height = invoice_height) 
    # Resize by height, comment the above line to use the original height
    # if original height is used, a scrollbar (or another method) should be implemented
    # or... we can resize but might need to rescale the bounding_box *probably* to get everything in absolute values
    # unless the images are also resized from the pdf
    
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # press 'r' to reset the window
    if key == ord("r"):
        image = clone.copy()
        list = []
        json_list = ''

    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break

# close all open windows
cv2.destroyAllWindows() 