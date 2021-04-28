import cv2
import numpy as np
import pandas as pd
import argparse

# Argument Parser for command Line image allocation
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Patch")
args = vars(ap.parse_args())
img_path = args['image']

# Reading image with opencv
img = cv2.imread(img_path)

# Global Variables
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# function to obtain x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


def getColorName(R, G, B):
    global cname
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(R - int(csv.loc[i, "G"])) + abs(R - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


while 1:
    cv2.imshow("image", img)
    if clicked:
        # cv2.rectangle(image, start point, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display (Color name and RGB values)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool))
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False

    # Break loop on ESC
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
