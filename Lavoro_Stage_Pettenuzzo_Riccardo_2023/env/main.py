import cv2 #lib for Computer Vision (opencv)
import numpy as np #lib for math and calculus
import flask #lib for web application
import rawpy #lib to read raw files as .cr2
from matplotlib import pyplot as plt


#Calculate the angular coefficient(M) of the straight line adjacent to the cut given the coordinates of two points
def Calculate_M_Adjacent_Line(x1, y1, x2, y2):
    return (y2 - y1)/(x2 - x1)


#Calculate the angular coefficient(M) of the vertical line given the angular coefficient(M) of another line
def Calculate_M_Perpendicular_Line(m):
    return -1/m


#Calculate the height(Q) of a line given his angular coefficient(M) and a point that belong the line
def Calculate_Q(m, x, y):
    return round(np.negative((m*x)) + y)


#Calculate the center coordinates of a segment given his coordinates
def Calculate_Segment_Mid_Coords(c1, c2):
    return round((c1 + c2) / 2)


#Calculate the intersection point between to line give their angular coefficient(M) and their height(Q)
def Calculate_Point_Intersection_Rays(m1, q1, m2, q2):
    q = np.negative(q1) + q2
    m = np.negative(m2) + m1
    x = round(q / m)
    y = round((m2*x)+q2)
    return(x, y)


#Calculate the width of the cut that's the length of the segment that is part of the vertical line that intersect the line adjacent to the cut
#give the coords of the intersection point and the point on the opposite side of the cut
def Calculate_Width(x1, x2, y1, y2):
    return np.sqrt(pow((x2-x1), 2)+pow((y2-y1), 2))


#Using all the methods above calculate the width of the cut
def Calculate_Width_Cut(segment_center, height, i):
    x1, y1, x2, y2 = 0, 0, 0, 0
    
    #check if the cut is not vertical or oblique
    try:
        #find the coords of one point adjacent to the cut
        for i in range(height):
            if thresh[segment_center-30, i] == 255 and thresh[segment_center-30, i+1] == 0:
                x1 = i
                y1 = segment_center-30
                break
        #find the coords of another point adjacent to the cut
        for i in range(height):
            if thresh[segment_center+30, i] == 255 and thresh[segment_center+30, i+1] == 0:
                x2 = i
                y2 = segment_center+30
                break
    except IndexError:
        return -1
    
    #draw the segment adjacent to the cut
    cv2.line(back_to_rgb, (x1, y1), (x2, y2), (0, 0,255), 2)

    #get the mid coords and draw a small line to highlight the center of the segment
    x_mid = Calculate_Segment_Mid_Coords(x1, x2)
    y_mid = Calculate_Segment_Mid_Coords(y1, y2)
    cv2.putText(back_to_rgb, str(i), (x_mid-40, y_mid), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA, False)
    cv2.line(back_to_rgb, (x_mid, y_mid), (x_mid-2, y_mid-2), (255, 0, 0), 2)

    x_opposite, y_opposite = 0, 0

    #find the coords of the dot on the opposite side of the cut
    for i in range(height):
        if thresh[y_mid, i] == 0 and thresh[y_mid, i+1] == 255:
            x_opposite = i
            y_opposite = y_mid
            break
    cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_opposite+5, y_opposite+5), (0, 255, 0), 2)

    #check if the cut is vertical then calculate the width of the cut adn return his width
    if x1 != x2:
        m1 = Calculate_M_Adjacent_Line(x1, y1, x2, y2)
        q1 = Calculate_Q(m1, x1, y1)
        m2 = Calculate_M_Perpendicular_Line(m1)
        q2 = Calculate_Q(m2, x_opposite, y_opposite)
        x_inters, y_inters = Calculate_Point_Intersection_Rays(m1, q1, m2, q2)
        print(*Get_Outline_Cut_Not_Vertical(m2, q2, x_opposite, x_inters, slab_grayscale))

        cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_inters, y_inters), (0, 0, 255), 2)
        return Calculate_Width(x_inters, x_opposite, y_inters, y_opposite)
    else:
        cv2.line(back_to_rgb, (x_mid, y_mid), (x_opposite, y_opposite), (0, 0, 255), 2)
        print(*Get_Outline_Cut_Vertical(x_opposite, x_mid, y_opposite, slab_grayscale))
        return x_opposite-x_mid


#Check if the cut is horizontal by iterating the height of the image and check if there'are black points that mean the cut not horizontal
def Check_Horizontal_Cut(width, height):
    x1, y1 = -1, -1
    try:
        for i in range(height):
            if thresh[round((width/2))-100, i] == 255 and thresh[round((width/2))-100, i+1] == 0:
                x1 = i
                y1 = -30
                break
    except IndexError:
        return True
    
    return False


#Iterate the process to get the width for all the height of cut to get more values and then better final value of width
#if there are not enough values to get the final width the image will be rotated
def Get_Width_Average():
    average = 0.0
    for k, v in segments.items():
        width_segment = Calculate_Width_Cut(v, height, k)
        print("Width Segment", width_segment, "px")
        if width_segment == -1 and k <= 4:
            return -1
        average = average + width_segment
        width_segment_list.append(width_segment)
        
    return average / len(segments)


#Get the difference between the first value and the last of all widths
def Get_Delta_Width():
    return width_segment_list[0] - width_segment_list[-1]


#Get the standard deviation from all the values of width of the cut
def Get_Standard_Deviation():
    return np.std(width_segment_list)


#Return a list o values that describe the outline/profile of the cut using the line the intersect the cut (y axis grey scale of the pixel,  x axis )
def Get_Outline_Cut_Not_Vertical(m_segment, q_segment, x_opposite, x_inters, grayscale_image):
    outline_values = []
    for i in range(x_inters-20, x_opposite+20):
        y = round((m_segment*i)+q_segment)
        outline_values.append(grayscale_image[y, i])
    plt.plot(outline_values, 'o-', color='blue', markersize=5)
    plt.show()
    return outline_values


#This method do the same thing of the method above but when the segment is vertical
def Get_Outline_Cut_Vertical(x_opposite, x_inters, height, grayscale_image):
    outline_values = []
    for i in range(x_inters-20, x_opposite+20):
        outline_values.append(grayscale_image[height, i])
    plt.plot(outline_values, 'o-', color='blue', markersize=5)
    plt.show()
    return outline_values



image_path = r"C:\Users\stage.upe4\Downloads\PXL_20230606_151247055.jpg"

#check if the file to read is jpg (or something else) cause raw files have different way to be read
if image_path.split(".")[-1] == "jpg":#if we need to read different type of image we can easy fix this by putting != "cr2"
    slab = cv2.imread(image_path)
elif image_path.split(".")[-1] == "cr2":
    raw = rawpy.imread(image_path) # access to the RAW image
    rgb = raw.postprocess() # a numpy RGB array
    slab = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


slab_grayscale = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY) #converting the image to grey scale
#slab_grayscale_blur = cv2.medianBlur(slab_grayscale, 15)
ret, thresh = cv2.threshold(slab_grayscale, 70, 255, cv2.THRESH_BINARY) #filtering the image
#thresh = cv2.adaptiveThreshold(slab_grayscale_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 55)
back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB) #converting the image to RGB
width, height = thresh.shape #getting image's dimensions

#fgbg = cv2.createBackgroundSubtractorMOG2()
#fgmask = fgbg.apply(thresh)
#can be useful when the image is not a piece of paper

#define list of width to get Standard Deviation and Delta_Width
width_segment_list = []

#define the center of all segments that will be adjacent 
segments = {
    0 : round((width)*.1),
    1 : round((width)*.2),
    2 : round((width)*.3),
    3 : round((width)*.4),
    4 : round((width/2)),
    5 : round((width)*.6),
    6 : round((width)*.7),
    7 : round((width)*.8),
    8 : round((width)*.9)
}

#Check if the cut is horizontal using the method then rotate the image and get his width
if Check_Horizontal_Cut(width, height):
    print("Was Horizontal")
    image_rotated = cv2.rotate(slab, cv2.ROTATE_90_CLOCKWISE)
    slab_grayscale = cv2.cvtColor(image_rotated, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)
    back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    width, height = thresh.shape[1], thresh.shape[0]

width_average = Get_Width_Average()

#if the average is not -1 it means that there were enough values to get the final width
#if not the image will be rotated and the process to get all width values will restart
if width_average == -1:
    print("Was Horizontal")
    image_rotated = cv2.rotate(slab, cv2.ROTATE_90_CLOCKWISE)
    slab_grayscale = cv2.cvtColor(image_rotated, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)
    back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    width, height = thresh.shape[1], thresh.shape[0]
    width_average = Get_Width_Average()

#printing all necessary values
print("Width Average", width_average, "px")
print("Delta Width", Get_Delta_Width(), "px")
print("Standard Deviation", Get_Standard_Deviation(), "px")
#here finishes the first method to get width average, delta width and standard deviation

#here start the second method to get width average, delta width and standard deviation

#displaying the image with some values drawn
cv2.imshow("Image", back_to_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()