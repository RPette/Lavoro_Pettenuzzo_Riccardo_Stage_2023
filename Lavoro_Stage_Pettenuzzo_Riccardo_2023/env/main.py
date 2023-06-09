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
    return np.negative((m*x)) + y


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
    cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_opposite+5, y_opposite), (0, 255, 0), 2)

    #check if the cut is vertical then calculate the width of the cut adn return his width
    if x1 != x2:
        m1 = Calculate_M_Adjacent_Line(x1, y1, x2, y2)
        q1 = Calculate_Q(m1, x1, y1)
        m2 = Calculate_M_Perpendicular_Line(m1)
        angular_coefficient_list.append(m2)
        q2 = Calculate_Q(m2, x_opposite, y_opposite)
        quote_list.append(q2)
        x_inters, y_inters = Calculate_Point_Intersection_Rays(m1, q1, m2, q2)
        #print(*Get_Outline_Cut_Not_Vertical(m2, q2, x_opposite, x_inters, slab_grayscale))

        cv2.line(back_to_rgb, (x_opposite, y_opposite), (x_inters, y_inters), (0, 0, 255), 2)
        return Calculate_Width(x_inters, x_opposite, y_inters, y_opposite)
    else:
        cv2.line(back_to_rgb, (x_mid, y_mid), (x_opposite, y_opposite), (0, 0, 255), 2)
        #print(*Get_Outline_Cut_Vertical(x_opposite, x_mid, y_opposite, slab_grayscale))
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
    for k, v in segments_width.items():
        width_segment = Calculate_Width_Cut(v, height, k)
        print("Width Segment", width_segment, "px")
        if width_segment == -1 and k <= 4:
            return -1
        average = average + width_segment
        width_segment_list.append(width_segment)
        
    return average / len(segments_width)


#Get the difference between the first value and the last of all widths
def Get_Delta_Width():
    return width_segment_list[0] - width_segment_list[-1]


#Get the standard deviation from all the values of width of the cut
def Get_Standard_Deviation():
    return np.std(width_segment_list)



image_path = r"C:\Users\stage.upe4\Desktop\Stefano\grigia_ob_resized.jpg"

#check if the file to read is jpg (or something else) cause raw files have different way to be read
if image_path.split(".")[-1] == "jpg":#if we need to read different type of image we can easy fix this by putting != "cr2"
    slab = cv2.imread(image_path)
elif image_path.split(".")[-1] == "cr2":
    raw = rawpy.imread(image_path) # access to the RAW image
    rgb = raw.postprocess() # a numpy RGB array
    slab = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


slab_grayscale = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY) #converting the image to grey scale
#slab_grayscale_blur = cv2.GaussianBlur(slab_grayscale, (19, 19), 0)
slab_grayscale_blur = cv2.medianBlur(slab_grayscale, 19)
#grigia = 50, rossa = 40
ret, thresh = cv2.threshold(slab_grayscale_blur, 50, 255, cv2.THRESH_BINARY) #filtering the image 
#thresh = cv2.adaptiveThreshold(slab_grayscale_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB) #converting the image to RGB
width, height = thresh.shape #getting image's dimensions

#define list of width to get Standard Deviation and Delta_Width

angular_coefficient_list = []
quote_list = []
width_segment_list = []

#define the center of all segments that will be adjacent 
segments_width = {
    1 : round((width)*.1),
    2 : round((width)*.2),
    3 : round((width)*.3),
    4 : round((width)*.4),
    5 : round((width/2)),
    6 : round((width)*.6),
    7 : round((width)*.7),
    8 : round((width)*.8),
    9 : round((width)*.9),
}

#Check if the cut is horizontal using the method then rotate the image and get his width
if Check_Horizontal_Cut(width, height):
    print("Was Horizontal, then rotated")
    image_rotated = cv2.rotate(slab, cv2.ROTATE_90_CLOCKWISE)
    slab_grayscale = cv2.cvtColor(image_rotated, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)
    back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    width, height = thresh.shape[1], thresh.shape[0]

width_average = Get_Width_Average()

#if the average is not -1 it means that there were enough values to get the final width
#if not the image will be rotated and the process to get all width values will restart
if width_average == -1:
    print("Not enough points to calculate width, then rotated")
    image_rotated = cv2.rotate(slab, cv2.ROTATE_90_CLOCKWISE)
    slab_grayscale = cv2.cvtColor(image_rotated, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)
    back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    width, height = thresh.shape[1], thresh.shape[0]
    width_average = Get_Width_Average()

#printing all necessary values

#here finishes the first method to get width average, delta width and standard deviation

#here start the second method to get width average, delta width and standard deviation
m_averaged = np.average(angular_coefficient_list)
q_averaged = np.average(quote_list)

segments_width2 = {
    0 : round((width/2)),
    1 : round((width)*.4),
    2 : round((width)*.3),
    3 : round((width)*.2),
    4 : round((width)*.1),
    5 : round((width)*.01),
    6 : round((width)*-.1),
    7 : round((width)*-.2),
    8 : round((width)*-.3),
    9 : round((width)*-.4),
    10 : round(-(width/2)),
}

outline_info = {
    0 : [],
    1 : [],
    2 : [],
    3 : [],
    4 : [],
    5 : [],
    6 : [],
    7 : [],
    8 : [],
    9 : [],
    10 : [],
}

outline_info_approx = {
    0 : [],
    1 : [],
    2 : [],
    3 : [],
    4 : [],
    5 : [],
    6 : [],
    7 : [],
    8 : [],
    9 : [],
    10 : [],
}

grayscale_pixel_value = []

x_coords = []
y_coords = []

back_to_rgb2 = cv2.cvtColor(slab_grayscale, cv2.COLOR_GRAY2RGB)

#this "method" shows the outline for all the width of the image and then draw a line that displays on the image where the outline pass
for k, v in segments_width2.items():
    grayscale_pixel_value=[]
    x_coords=[]
    y_coords=[]
    for i in range(height):
        y = round((m_averaged*i)+q_averaged)
        if y-v > 0:
            try:
                grayscale_pixel_value.append(slab_grayscale[y-v, i])
            except Exception as e:
                print(e)
            else:
                x_coords.append(i)
                y_coords.append(y-v)
    try:
        cv2.line(back_to_rgb2, (x_coords[0], y_coords[0]), (x_coords[-1], y_coords[-1]), (255, 0, 255), 2)
    except IndexError as ie:
        print(ie)
    else:
        outline_info[k].append(grayscale_pixel_value)
        outline_info[k].append(x_coords)
        outline_info[k].append(y_coords)

#this method approximate the profile where the values in grayscale is high and if the difference between the value in that index and the next index is lower than a constant
#it means that this value can be approximated with others and we obtain a profile with simplified values where it's not necessary to calculate width
for k, v in outline_info.items():
    try:
        outline = v[0]
        x_coords2 = v[1]
    except IndexError as ie:
        print(ie)
    else:
        new_grayscale_pixel_values = []
        x_coords_approx = []
        values_to_approx = []
        start_index = 0
        finish_index = 0
        starting_or_finishing = True
        for i in range(len(x_coords2)+1):
            x_coords_approx.append(i)
            try:
                if np.positive(outline[i] - outline[i+1]) <= 40 and outline[i] >= 75:
                    values_to_approx.append(outline[i])
                    if starting_or_finishing:
                        start_index = i
                        starting_or_finishing = not starting_or_finishing
                elif starting_or_finishing:
                    new_grayscale_pixel_values.insert(i, outline[i])
                else:
                    finish_index = i
                    starting_or_finishing = not starting_or_finishing
                    approx_grayscale_value = round(np.average(values_to_approx))
                    for j in range(start_index, finish_index+1):
                        new_grayscale_pixel_values.insert(j, approx_grayscale_value)
            except IndexError as ie:
                print(ie)
    
    outline_info_approx[k].append(new_grayscale_pixel_values)
    outline_info_approx[k].append(x_coords_approx)

print(*new_grayscale_pixel_values)
#this method plot the first profile and the last to see the difference
for k in outline_info:
    try:
        plt.plot(outline_info[k][0], '*-', color='purple', markersize=6)
        plt.plot(outline_info[10][0], 'o-', color='blue', markersize=4)
        mng = plt.get_current_fig_manager()
        mng.resize(1700, 700)
        mng.set_window_title(str(k))
        plt.show()
    except Exception as e:
        print(e)
    else:
        break

#this method take the grayscale values, and their coords that were not approximated and goes back and take some values before and after the largest ray of low values
#than check where the value before and after take the average of the lowest values and get the coords where the value is at least 30 in grayscale higher 
#than get the width between those points
for k, v in outline_info_approx.items():
    try:
        outline_approx = v[0]
        x_coords3 = v[1]
        outline_final = []
        for i in range(len(v[1])+1):
            if outline_approx[i] >= 130:
                outline_final.insert(i, -1)
            else:
                outline_final.insert(i, outline_approx[i])
    except Exception as e:
        print(e)
    
    print(*outline_final)
    outline_lower_values_width = []
    start_finish = True
    width_number = 0
    for i in range(len(outline_final)+1):
        try:
            if outline_final[i] != -1:
                for i in range(i, len(outline_final)+1):
                    if outline_final[i] != -1:
                        width_number += 1
                    else: 
                        break
        except Exception as e:
            print(e)
        else:
            outline_lower_values_width.append(width_number)
            width_number = 0
        
    
    print(*outline_lower_values_width)

#displaying the image with some values drawn
print("Width Average", width_average, "px")
print("Delta Width", Get_Delta_Width(), "px")
print("Standard Deviation", Get_Standard_Deviation(), "px")
cv2.imshow("Image 2° method", back_to_rgb2)
cv2.imshow("Image 1° method", back_to_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()