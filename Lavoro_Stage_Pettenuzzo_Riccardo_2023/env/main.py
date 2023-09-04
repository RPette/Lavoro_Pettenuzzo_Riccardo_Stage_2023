import cv2 #lib for Computer Vision (opencv)
import numpy as np #lib for math and calculus
import rawpy #lib to read raw files as .cr2
from matplotlib import pyplot as plt #lib for displaying graphs and plots

#TODO summarize methods also in italian

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
        q2 = Calculate_Q(m2, x_opposite, y_opposite)
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
def Get_Delta_Width(width_list):
    try:
        return np.positive(width_list[0] - width_list[-1])
    except IndexError as ie:
        print(ie)


#Get the standard deviation from all the values of width of the cut
def Get_Standard_Deviation(width_list):
    return np.std(width_list)


image_path = r"C:\Users\stage.upe4\Desktop\Stefano\grigia_ob_resized.jpg"

#check if the file to read is jpg (or something else) cause raw files have different way to be read
if image_path.split(".")[-1] == "jpg":#if we need to read different type of image we can easy fix this by putting != "cr2"
    slab = cv2.imread(image_path)
elif image_path.split(".")[-1] == "cr2":
    raw = rawpy.imread(image_path) # access to the RAW image
    rgb = raw.postprocess() # a numpy RGB array
    slab = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


slab_grayscale = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY) #converting the image to gray scale
slab_grayscale2 = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY)#converting the image to gray scale for the second method
#slab_grayscale_blur = cv2.GaussianBlur(slab_grayscale, (19, 19), 0)
slab_grayscale_blur = cv2.medianBlur(slab_grayscale, 19)
#grigia = 50, rossa = 40
ret, thresh = cv2.threshold(slab_grayscale_blur, 40, 255, cv2.THRESH_BINARY) #filtering the image 
#thresh = cv2.adaptiveThreshold(slab_grayscale_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
back_to_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB) #converting the image to RGB
width, height = thresh.shape #getting image's dimensions

#TODO using cv2.findContours after filtering the image, i can take all the area inside the contours and the largest area is probably the cut
#TODO then i can put it on a full white image and proceed with the 1° method to get width, delta width and standard deviation 

#define list of width to get Standard Deviation and Delta_Width
width_segment_list = []

#define the center of all segments that will be adjacent 
segments_width = {
    1 : round((width)*.1),
    2 : round((width)*.2),
    3 : round((width)*.3),
    4 : round((width)*.4),
    5 : round((width)*.5),
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

#print("1° Method Results")
#print("Width Average", width_average, "px")
#print("Delta Width", Get_Delta_Width(width_segment_list), "px")
#print("Standard Deviation", Get_Standard_Deviation(width_segment_list), "px")
#cv2.imshow("Image 1° method", back_to_rgb)
##cv2.imwrite(r"C:\Users\stage.upe4\Desktop\image.jpg", back_to_rgb)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#HERER FINISHES the first method to get width average, delta width and standard deviation that depends from threshold

#TODO check every try except in the code and where is possible replace it with if closure

#HERER STARTS the second method to get width average, delta width and standard deviation from the grayscale using outlines, getting width from the lowest part of every outline
#and using width at half-height

#dict that specify the translation factor to get outlines at different height
segments_width2 = {
    0 : round((width/2)),
    1 : round((width)*.1),
    2 : round((width)*.3),
    3 : round((width)*.2),
    4 : round((width)*.4),
    5 : round((width)*.58),
    6 : round((width)*.01),
    7 : round((width)*-.1),
    8 : round((width)*-.2),
    9 : round((width)*-.3),
    10 : round((width)*-.4),
    11 : round((width)*-.58),
    12 : round(-(width/2)),
}

#dict that stores every outline with his grayscale values, x-coords and y-coords
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
    11 : [],
    12 : [],
}

#dict that stores all approximated outlines and their x-coords
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
    11 : [],
    12 : [],
}

#dict that stores every spike of grayscale values of the outline
outline_spikes_infos = {
}

#dict that stores the length of every spike took from the last dict
length_lowest_part = {
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
    11 : [],
    12 : [],
}

#dict that stores the outline's grayscale values near to the cut and also the starting and finish point of the cut
outline_on_the_cut = {
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
    11 : [],
    12 : [],
}

#dict that stores the outline's grayscale approximated values near to the cut
outline_on_cut_approx = {
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
    11 : [],
    12 : [],
}

#defining variable and list to store values
grayscale_pixel_value = []#list to store the gray scale values of a pixel at that coords

width_lowest_part_average = []#list to store the width of every outline on the cut at the lowest part of the cut

width_half_height_average = []#list to store the width of every outline on the cut at half-height

x_coords = []#list to store x-coords of a pixel in the image

y_coords = []#list to store y-coords of a pixel in the image

half_height = -1#half-height to get width at this height

back_to_rgb2 = cv2.cvtColor(slab_grayscale2, cv2.COLOR_GRAY2RGB)#converting the gray scale image to rgb to draw lines
print(height, width)

#I need to make independent the second method to the second, so this method checks the first line of the grayscale image and the last
#when it finds the longest line of black pixels it takes the mid of both and take the angular coefficient and the quote, than take the perpendicular coefficient
first_line_grayscale_values = []#list to store the gray scale values on top of image
last_line_grayscale_values = []#list to store gray scale values on bottom of image

first_last_spike_start = -1#variable that stores the start coord of the spike on both top and bottom side of image
first_last_spike_finish = -1#variable that stores the finish coord of the spike on both top and bottom side of image

starting_or_finishing_first = False#boolean value that says when the spike start and when it finishes on top of image
starting_or_finishing_last = False#boolean value that says when the spike start and when it finishes on bottom of image

#dict that associate the start, finish and length of spike on top of image
first_line_spike_data = {
}

#dict that associate the start, finish and length of spike on bottom of image
last_line_spike_data = {
}

first_line_spike_lengths = []#list to store the length of every spike on top of image
last_line_spike_lengths = []#list to store the length of every spike on bootom of image

cut_first_line_mid = -1#variable used to store the coord of the mid point on the cut on top of image
cut_last_line_mid = -1#variable used to store the coord of the mid point on the cut on bottom of image

key = 0#key used to assign the on the dict that store the start, finish and length of a spike

#taking grayscale values of the first line of the image (on top of image)
for i in range(height):
    try:
        if slab_grayscale2[0, i] <= 100:
            first_line_grayscale_values.insert(i, slab_grayscale2[0, i])
        else:
            first_line_grayscale_values.insert(i, 255)
    except IndexError as ie:
        print(ie)
plt.plot(first_line_grayscale_values, 'o-', color='blue', markersize=4)
mng = plt.get_current_fig_manager()
mng.resize(1700, 700)
mng.set_window_title("First Line")
plt.show()

#taking grayscale values of the last line (on bottom of image)
for i in range(height):
    try:
        if slab_grayscale2[-1, i] <= 100:
            last_line_grayscale_values.insert(i, slab_grayscale2[-1, i])
        else:
            last_line_grayscale_values.insert(i, 255)
    except IndexError as ie:
        print(ie)
plt.plot(last_line_grayscale_values, 'o-', color='red', markersize=4)
mng = plt.get_current_fig_manager()
mng.resize(1700, 700)
mng.set_window_title("Last Line")
plt.show()

#TODO take all the pixel that passes for the two mid coords took from the first and the last line, if the pixels that passes for the line are all near each other for their grayscale values other it's the correct line
#TODO if not i need to change the segment of semi black pixels

#taking from the top of image the start, finish and length of every spike in gray scale values, and putting all the lengths to a list to then take the highest
for i in range(len(first_line_grayscale_values)):
    try:
        if first_line_grayscale_values[i] != 255 and not starting_or_finishing_first:
            first_last_spike_start = i
            starting_or_finishing_first = not starting_or_finishing_first
        elif first_line_grayscale_values[i] == 255 and starting_or_finishing_first:
            first_last_spike_finish = i
            starting_or_finishing_first = not starting_or_finishing_first
            first_line_spike_data[key] = [first_last_spike_start]
            first_line_spike_data[key].append(first_last_spike_finish)
            first_line_spike_data[key].append(np.positive(first_last_spike_finish - first_last_spike_start))
            first_line_spike_lengths.append(np.positive(first_last_spike_finish - first_last_spike_start))
            key += 1
            first_last_spike_start = -1
            first_last_spike_finish = -1
    except IndexError as ie:
        print(ie)

#sorting the lengths list to then take the highest
first_line_spike_lengths.sort(reverse=True)

#iterating the dict to get the coords of the longest spike on top
for k, v in first_line_spike_data.items():
    if v[2] == first_line_spike_lengths[0]:
        cut_first_line_mid = Calculate_Segment_Mid_Coords(v[0], v[1])
        
#clearing variable for the bottom of the image
first_last_spike_start = -1
first_last_spike_finish = -1
key = 0

#taking from the bootom of image the start, finish and length of every spike in gray scale values, and putting all the lengths to a list to then take the highest
for i in range(len(last_line_grayscale_values)):
    try:
        if last_line_grayscale_values[i] != 255 and not starting_or_finishing_last:
            first_last_spike_start = i
            starting_or_finishing_last = not starting_or_finishing_last
        elif last_line_grayscale_values[i] == 255 and starting_or_finishing_last:
            first_last_spike_finish = i
            starting_or_finishing_last = not starting_or_finishing_last
            last_line_spike_data[key] = [first_last_spike_start]
            last_line_spike_data[key].append(first_last_spike_finish)
            last_line_spike_data[key].append(np.positive(first_last_spike_finish - first_last_spike_start))
            last_line_spike_lengths.append(np.positive(first_last_spike_finish - first_last_spike_start))
            key += 1
            first_last_spike_start = -1
            first_last_spike_finish = -1
    except IndexError as ie:
        print(ie)

#sorting the lengths list to then take the highest
last_line_spike_lengths.sort(reverse=True)

#iterating the dict to get the coords of the longest spike on top
for k, v in last_line_spike_data.items():
    if v[2] == last_line_spike_lengths[0]:
        cut_last_line_mid = Calculate_Segment_Mid_Coords(v[0], v[1])

#calculating the angular coefficient of the line that passes throughout the two mid points
m_cut = Calculate_M_Adjacent_Line(cut_first_line_mid, 0, cut_last_line_mid, width)
#calculating the perpendicular angular coefficient of the line to then take the quote and then shift the line up and down on the image to get different line on the image
m_cut = Calculate_M_Perpendicular_Line(m_cut)
#calculating the quote of the line
q_cut = Calculate_Q(m_cut, 0, width/2)


#this "method" shows the outline for all the width of the image and then draw a line that displays on the image where the outline pass
#then associate x-coords, y-coords and grayscale values for every line in a dict
for k, v in segments_width2.items():
    grayscale_pixel_value=[]
    x_coords=[]
    y_coords=[]
    for i in range(height):
        y = round((m_cut*i)+q_cut)
        if y-v > 0:
            try:
                grayscale_pixel_value.append(slab_grayscale2[y-v, i])
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
#then associate the approximated gray scale values of the line and his x-coords in a dict
for k, v in outline_info.items():
    try:
        outline = v[0]#gray scale values of the outline
        x_coords2 = v[1]#x-coords of every point
        new_grayscale_pixel_values = []#defining the list to store new approximated gray scale values of the outline
        x_coords_approx = []#list to store x-coords of the approx outline
        values_to_approx = []#list to store all the values the need to be approximated
        start_index = 0#variable that store start index of values that need to be approximated
        finish_index = 0#variable that store finish index of values that need to be approximated
        starting_or_finishing = True#boolean variable that says when the values that need to sbe approximated start and when it finishes
    except IndexError as ie:
        print(ie)
    else:
        for i in range(len(x_coords2)+1):
            x_coords_approx.append(i)
            try:
                if np.positive(outline[i] - outline[i+1]) <= 40 and outline[i] >= 100:
                    values_to_approx.append(outline[i])
                    if starting_or_finishing:
                        start_index = i
                        starting_or_finishing = not starting_or_finishing
                elif starting_or_finishing:
                    new_grayscale_pixel_values.insert(i, outline[i])
                else:
                    finish_index = i
                    starting_or_finishing = not starting_or_finishing
                    for j in range(start_index, finish_index+1):
                        if len(values_to_approx) >= 3:
                            new_grayscale_pixel_values.insert(j, -1)
                        else:
                            new_grayscale_pixel_values.insert(j, outline[j])
            except IndexError as ie:
                print(ie)         
        outline_info_approx[k].append(new_grayscale_pixel_values)
        outline_info_approx[k].append(x_coords_approx)

#this method takes all the approximated lists of grayscale pixel and take all the start and finish index where the line where not approximated
#it associate the starting index, the finish index and the length where the values are low, then it appends to another list the lengths and calculate the higher for every line
for k, v in outline_info_approx.items():
    try:
        outline_approx = v[0]#list to store the approximated gray scale values of the outline
        start_index = 0#variable that stores the start index of the spike
        finish_index = 0#variable that stores the finish index of the spike
        started_finished = False#boolean variable that says when the spike start and when it finishes
    except IndexError as e:
        print(e)
    else:
        for i in range(len(outline_approx)+1):
            try:
                if (outline_approx[i] != -1 and outline_approx[i+1] == -1) and started_finished:
                    finish_index = i
                    started_finished = not started_finished
                    outline_spikes_infos[k, i] = [start_index+1, finish_index, finish_index-start_index]
                    length_lowest_part[k].append((finish_index-start_index))
                    start_index = 0
                    finish_index = 0
                elif (outline_approx[i] == -1 and outline_approx[i+1] != -1) and not started_finished:
                    start_index = i
                    started_finished = not started_finished
            except IndexError as ie:
                print(ie)
        
        length_lowest_part[k].sort(reverse=True)

#this part takes the indexes of the lowest part of the whole outline and take some pixel before and after than associate new start, finish and gray scale values on the cut to a dict
for k, v in length_lowest_part.items():
    try:
        longest_width_start = -1#variable that store the starting index of the longest and deepest spike 
        longest_width_finish = -1#variable that store the finishing index of the longest and deepest spike 
        deepest_spike_values = []#list that store the gray scale values of the longest and deepest spike of the outline
        for l, m in outline_spikes_infos.items():
            if l[0] == k and m[2] == v[0]:
                longest_width_start = m[0]
                longest_width_finish = m[1]
                break
        for i in range(longest_width_start-10, longest_width_finish+11):
            deepest_spike_values.append(outline_info[k][0][i])
    except IndexError as ie:
        print(ie)
    else:
        outline_on_the_cut[k].append(deepest_spike_values)
        outline_on_the_cut[k].append(10)
        outline_on_the_cut[k].append(len(deepest_spike_values)-11)
        #plt.plot(deepest_spike_values, 'o-', color='blue', markersize=4)
        #mng = plt.get_current_fig_manager()
        #mng.resize(1700, 700)
        #mng.set_window_title(str(k))
        #plt.show()

#this part of method calculate the average of the lowest values, and the highest value near the borders of the cut
#to get then the half height to measure the width on it
for k, v in outline_on_the_cut.items():
    try:
        outline_complete = v[0]#list to store gray scale values of the outline on the cut
        start = v[1]#variable that store the start index of the outline
        finish = v[2]#variable that store the finish index of the outline
        outline_lowest_values = []#list that store all the lowest values of the cut to make the average to then get the lowest for the half-height
        highest_value = -1#variable that store the highest value on right or left, after or before the spike
        for i in range(start, finish+1):
            if outline_complete[i] <= 75:
                    outline_lowest_values.append(outline_complete[i])
        for j in range(0, finish+1):
            if np.positive(outline_complete[j] - outline_complete[j+1]) >= 100:
                highest_value = outline_complete[j+1]
        for h in range(start+1, len(outline_complete)):
            if np.positive(outline_complete[h] - outline_complete[h+1]) >= 100:
                if outline_complete[h+1] > highest_value:
                    highest_value = outline_complete[h+1]
    except Exception as ie:
        print(ie)
    try:
        width_lowest_part_average.append(len(outline_lowest_values))
        lowest_value = round(np.average(outline_lowest_values))
        half_height = round((highest_value-lowest_value)/2)
    except Exception as e:
        print(e)
        

#this method tries to approx the highest values of the outline so then i can calculate the width at half-height the associate the gray scale values the start and finish in a dict
#then i can take only the longest way of pixels that are not 255
for k, v in outline_on_the_cut.items():
    try:
        outline_complete_approx = []#list to store the approximated outline on the cut
        outline_complete = v[0]#list to store gray scale values of the outline on the cut
        start = v[1]#variable that store the start index of the outline
        finish = v[2]#variable that store the finish index of the outline
        for i in range(0, len(outline_complete)+1):
            if outline_complete[i] <= half_height:
                outline_complete_approx.insert(i, outline_complete[i])
            elif np.positive(outline_complete[i] - outline_complete[i+1]) <= 50 and (outline_complete[i] <= 255 and outline_complete[i] >= half_height):
                outline_complete_approx.insert(i, 255)
            else:
                outline_complete_approx.insert(i, 255)
    except Exception as e:
        print(e)
    outline_on_cut_approx[k].append(outline_complete_approx)
    outline_on_cut_approx[k].append(start)
    outline_on_cut_approx[k].append(finish)

#this method checks where the half-height pass a segment from two point, then calculate the ray that pass for those two point and find x when y = half-height
#i can try to check the length of all the segment that intersect the half-height ray and choose the longest or the nearest to the start and finish index
#it works sometimes but to make it work everytime i can try to approximate to a value all the points that are not in the cut
for k, v in outline_on_the_cut.items():
    try:
        outline_complete = v[0]#list to store gray scale values of the outline on the cut
        start = v[1]#variable that store the start index of the outline
        finish = v[2]#variable that store the finish index of the outline
        half_height_start = -1#variable that store the start value where the half-height line intersect the segment of the cut
        half_height_finish = -1#variable that store the finish value where the half-height line intersect the segment of the cut
        m_segment = -1#variable that store the angular coefficient of the ray that is intersected from the half-height
        q_segment = -1#variable that store the quote of the ray that is intersected from the half-height
        new_start = -1#variable that store the start index to start iterating to get the second segment that intersect the half-height
        for i in range(0, start+5):
            if half_height <= max(outline_complete[i], outline_complete[i+1]) and half_height >= min(outline_complete[i], outline_complete[i+1]) and np.positive(outline_complete[i]-outline_complete[i+1]) >= 80:
                m_segment = Calculate_M_Adjacent_Line(i, outline_complete[i], i+1, outline_complete[i+1])
                q_segment = Calculate_Q(m_segment, i, outline_complete[i+1])
                half_height_start = (half_height - q_segment)/m_segment
                new_start = i
        for j in range(new_start, len(outline_complete)):
            if half_height <= max(outline_complete[j], outline_complete[j+1]) and half_height >= min(outline_complete[j], outline_complete[j+1]) and np.positive(outline_complete[j]-outline_complete[j+1]) >= 80:
                m_segment = Calculate_M_Adjacent_Line(j, outline_complete[j], j+1, outline_complete[j+1])
                q_segment = Calculate_Q(m_segment, j, outline_complete[j+1])
                half_height_finish = (half_height - q_segment)/m_segment  
    except IndexError as e:
        print(e)
    try:              
        width_half_height_average.append(half_height_finish-half_height_start)
    except Exception as e:
        print(e)

print("2° Method Results from Width at Half-Height")
print("Width Average", np.average(width_half_height_average), "px")
print("Delta Width", Get_Delta_Width(width_half_height_average), "px")
print("Standard Deviation", Get_Standard_Deviation(width_half_height_average), "px\n")

print(len(width_half_height_average), len(width_lowest_part_average))
    

#this part of method plots the part of the outline near the cut
for k, v in outline_on_the_cut.items():
    #plt.plot(outline_on_cut_approx[k][0], '+-', color='green', markersize=6)
    try:
        plt.plot(v[0], 'o-', color='blue', markersize=4)
        plt.plot(outline_on_cut_approx[k][0], '+-', color='red', markersize=6)
        mng = plt.get_current_fig_manager()
        mng.resize(1700, 700)
        mng.set_window_title(str(k))
        plt.show() 
    except Exception as e:
        print(e)

#printing 2° method with results from lowest part of outline
print("2° Method Results from lowest part of outline")
print("Width Average", np.average(width_lowest_part_average), "px")
print("Delta Width", Get_Delta_Width(width_lowest_part_average), "px")
print("Standard Deviation", Get_Standard_Deviation(width_lowest_part_average), "px\n")

#this method plot the first profile and the last to see the difference of the not approx lines
for k in outline_info.keys():
    try:
        #plt.plot(outline_info[k][0], '*-', color='purple', markersize=6)
        #plt.plot(outline_info[10][0], 'o-', color='blue', markersize=4)
        mng = plt.get_current_fig_manager()
        mng.resize(1700, 700)
        mng.set_window_title(str(k))
        #lt.show()
    except Exception as e:
        print(e)
    else: break

#displaying the image with some values drawn
#printing 1° method results
print("1° Method Results")
print("Width Average", width_average, "px")
print("Delta Width", Get_Delta_Width(width_segment_list), "px")
print("Standard Deviation", Get_Standard_Deviation(width_segment_list), "px")
cv2.imshow("Image 2° method", back_to_rgb2)
cv2.imshow("Image 1° method", back_to_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()