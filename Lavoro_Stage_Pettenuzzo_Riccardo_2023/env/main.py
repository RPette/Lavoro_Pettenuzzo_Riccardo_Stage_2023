import cv2
import numpy as np
import flask
from PIL import Image


def Calculate_M_Adjacent_Ray(x1, y1, x2, y2):
    return (y2 - y1)/(x2 - x1)


def Calculate_M_Perpendicular_Ray(m):
    return -1/m


def Calculate_Q(m, x, y):
    return round(np.negative((m*x)) + y)

    
def Calculate_Segment_Mid_Coords(c1, c2):
    return round((c1 + c2) / 2)


def Calculate_Point_Intersection_Rays(m1, q1, m2, q2):
    q = np.negative(q1) + q2
    m = np.negative(m2) + m1
    x = round(q / m)
    y = round((m2*x)+q2)
    return(x, y)


def Calculate_Width(x1, x2, y1, y2):
    return round(np.sqrt(pow((x2-x1), 2)+pow((y2-y1), 2)))


def Calculate_Width_Cut(segment_center, height):
    x1, y1, x2, y2 = 0, 0, 0, 0
    
    #find the coords of one dot adjacent to the cut
    for i in range(height):
        if thresh[segment_center-30, i] == 255 and thresh[segment_center-30, i+1] == 0:
            x1 = i
            y1 = segment_center-30
            break
    #find the coords of another dot adjacent to the cut
    for i in range(height):
        if thresh[segment_center+30, i] == 255 and thresh[segment_center+30, i+1] == 0:
            x2 = i
            y2 = segment_center+30
            break

    cv2.line(back_to_rgb, (x1, y1), (x2, y2), (0, 0,255), 2)

    x_mid = Calculate_Segment_Mid_Coords(x1, x2)
    y_mid = Calculate_Segment_Mid_Coords(y1, y2)
    cv2.line(back_to_rgb, (x_mid, y_mid), (x_mid-2, y_mid-2), (255, 0, 0), 2)

    x_opposite, y_opposite = 0, 0

    #find the coords of the dot on the opposite side of the cut
    for i in range(height):
        if thresh[y_mid, i] == 0 and thresh[y_mid, i+1] == 255:
            x_opposite = i
            y_opposite = y_mid
            break
    cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_opposite+5, y_opposite+5), (0, 255, 0), 2)

    #Calculating the width of the cut
    if x1 != x2:
        m1 = Calculate_M_Adjacent_Ray(x1, y1, x2, y2)
        q1 = Calculate_Q(m1, x1, y1)
        m2 = Calculate_M_Perpendicular_Ray(m1)
        q2 = Calculate_Q(m2, x_opposite, y_opposite)
        x_inters, y_inters = Calculate_Point_Intersection_Rays(m1, q1, m2, q2)

        cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_inters, y_inters), (0, 0, 255), 2)
        return Calculate_Width(x_inters, x_opposite, y_inters, y_opposite)
    else:
        cv2.line(back_to_rgb, (x_mid, y_mid), (x_opposite, y_opposite), (0, 0, 255), 2)
        return x_opposite-x_mid


def Get_Width_Average():
    average = 0.0
    for v in segments.values():
        average = average + Calculate_Width_Cut(v, height)
        
    return round(average / len(segments))


def Check_Horizontal_Cut(width, height):
    x1, y1 = -1, -1
    try:
        for i in range(height):
            if thresh[round((width/2))-200, i] == 255 and thresh[round((width/2))-200, i+1] == 0:
                x1 = i
                y1 = -30
                break
    except IndexError:
        return True
    
    return False


image_path = r"C:\Users\stage.upe4\Downloads\lastra_carta_orizzontale2.jpg"
slab = cv2.imread(image_path)
slab_grayscale = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)
back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

#fgbg = cv2.createBackgroundSubtractorMOG2()
#fgmask = fgbg.apply(thresh)
#can be useful when the image is not a piece of paper

width, height = thresh.shape

segments = {
    0 : round(width/2),
    1 : round((width/2)+80),
    2 : round((width/2)+160),
    3 : round((width/2)+240),
    4 : round((width/2)-80),
    5 : round((width/2)-160),
    6 : round((width/2)-240)
}

if Check_Horizontal_Cut(width, height):
    print("Was Horizontal")
    image = Image.open(image_path)
    rotated_image = image.rotate(90)
    rotated_image.save(image_path)
    slab = cv2.imread(image_path)
    slab_grayscale = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)
    back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    width, height = thresh.shape
    print("Width Average", Get_Width_Average(), "px")
else:
    print("Width Average", Get_Width_Average(), "px")
    

cv2.imshow("Image", back_to_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()    



















"""
    #find the coords of one dot adjacent to the cut
for i in range(height):
    if thresh[round((width/2)-30), i] == 255 and thresh[round((width/2)-30), i+1] == 0:
        x1 = i
        y1 = round((width/2)-30)
        break
#find the coords of another dot adjacent to the cut
for i in range(height):
    if thresh[round((width/2)+30), i] == 255 and thresh[round((width/2)+30), i+1] == 0:
        x2 = i
        y2 = round((width/2)+30)
        break

back_to_rgb = cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB)
cv2.line(back_to_rgb, (x1, y1), (x2, y2), (0, 0,255), 2)

x_mid = Calculate_Segment_Mid_Coords(x1, x2)
y_mid = Calculate_Segment_Mid_Coords(y1, y2)
x_opposite, y_opposite = 0, 0

#find the coords of the dot on the opposite side of the cut
for i in range(height):
        if thresh[y_mid, i] == 0 and thresh[y_mid, i+1] == 255:
            x_opposite = i
            y_opposite = y_mid
            break

cv2.line(back_to_rgb, (x_mid, y_mid), (x_mid-2, y_mid-2), (255, 0, 0), 2)
width_cut = 0

if x1 != x2:
    m1 = Calculate_M_Adjacent_Ray(x1, y1, x2, y2)
    q1 = Calculate_Q(m1, x1, y1)
    m2 = Calculate_M_Perpendicular_Ray(m1)
    q2 = Calculate_Q(m2, x_opposite, y_opposite)
    x_inters, y_inters = Calculate_Point_Intersection_Rays(m1, q1, m2, q2)
    
    cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_inters, y_inters), (0, 0, 255), 2)
    width_cut = Calculate_Width(x_inters, x_opposite, y_inters, y_opposite)
else:
    cv2.line(back_to_rgb, (x_mid, y_mid), (x_opposite, y_opposite), (0, 0, 255), 2)
    width_cut = x_opposite-x_mid

print("Spessore taglio in px :", width_cut)
    """



cv2.waitKey(0)
cv2.destroyAllWindows()