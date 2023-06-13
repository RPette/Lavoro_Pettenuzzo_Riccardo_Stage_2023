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
def Get_Delta_Width(width_list):
    return width_list[0] - width_list[-1]


#Get the standard deviation from all the values of width of the cut
def Get_Standard_Deviation(width_list):
    return np.std(width_list)



# sourcery skip: list-comprehension, move-assign-in-block, remove-dict-keys, use-dict-items
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

outline_spikes_infos = {
}


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
}

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
}

grayscale_pixel_value = []
width_lowest_part_average = []
width_half_height_average = []
x_coords = []
y_coords = []
half_height = -1

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
        new_grayscale_pixel_values = []
        x_coords_approx = []
        values_to_approx = []
        start_index = 0
        finish_index = 0
        starting_or_finishing = True
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
                    approx_grayscale_value = round(np.average(values_to_approx))
                    for j in range(start_index, finish_index+1):
                        if len(values_to_approx) >= 3:
                            new_grayscale_pixel_values.insert(j, -1)
                        else:
                            new_grayscale_pixel_values.insert(j, outline[j])
            except IndexError as ie:
                print(ie)         
        outline_info_approx[k].append(new_grayscale_pixel_values)
        outline_info_approx[k].append(x_coords_approx)

#this method takes alle the approximated lists of grayscale pixel and take all the start and finish index where the line where not approximated
#it associate the starting index, the finish index and the length where the values are low, then it appends to another list the lengths and calculate the higher for every line
#than it searches where the length is higher and take the starting index and the finish index, then it displays a plot for every line
#When I have the pixel where the length is higher and start and finish index, i've to take some values before and after the indexes to get a better view of the outline
for k, v in outline_info_approx.items():
    try:
        outline_approx = v[0]
        start_index = 0 
        finish_index = 0
        started_finished = False
        outline_lowest_spikes = []
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

#this part takes the indexes of the lowest part of the whole outline and take some pixel before and after
for k, v in length_lowest_part.items():
    try:
        longest_width_start = -1
        longest_width_finish = -1
        deepest_spike_values = []
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
        mng = plt.get_current_fig_manager()
        mng.resize(1700, 700)
        mng.set_window_title(str(k))
        #plt.show()

#this part of method calculate the average of the lowest values, and the highest value neat the borders of the cut
#to get then the half height to measure the width on it
for k, v in outline_on_the_cut.items():
    try:
        outline_complete = v[0]
        start = v[1]
        finish = v[2]
        outline_lowest_values = []
        highest_value = -1
        lowest_value = -1

        for i in range(start, finish+1):
            if outline_complete[i] <= 75:
                outline_lowest_values.append(outline_complete[i])
        for j in range(0, finish+1):
            if np.positive(outline_complete[j] - outline_complete[j+1]) >= 100:
                highest_value = outline_complete[j+1]
        for h in range(start+1, len(outline_complete)+1):
            if np.positive(outline_complete[h] - outline_complete[h+1]) >= 100:
                if outline_complete[h+1] > highest_value:
                    highest_value = outline_complete[h+1]
    except Exception as ie:
        print(ie)

    width_lowest_part_average.append(len(outline_lowest_values))
    lowest_value = round(np.average(outline_lowest_values))
    print(*outline_complete)
    print("N°", k, "Lowest Averaged", lowest_value, "Highest", highest_value)
    half_height = round((highest_value-lowest_value)/2)
    print(k, "Half Height", half_height, "\n")
#this method checks where the half-height pass a segment from two point, then calculate the ray that pass for those two point and find x when y = half-height
#i can try to check the lenght of all the segment that intersect the half-height ray and choose the longest or the nearest to the start and finish index
#it works sometimes but tho make it work i can try to approximate to a value all the points that are not in the cut
for k, v in outline_on_the_cut.items():
    try:
        outline_complete = v[0]
        start = v[1]
        finish = v[2]
        half_height_start = -1
        half_height_finish = -1
        m_segment = -1
        q_segment = -1
        new_start = -1
        for i in range(0, start+5):
            if half_height <= max(outline_complete[i], outline_complete[i+1]) and half_height >= min(outline_complete[i], outline_complete[i+1]) and np.positive(outline_complete[i]-outline_complete[i+1]) >= 80:
                m_segment = Calculate_M_Adjacent_Line(i, outline_complete[i], i+1, outline_complete[i+1])
                q_segment = Calculate_Q(m_segment, i, outline_complete[i+1])
                half_height_start = (half_height - q_segment)/m_segment
                new_start = i
        for j in range(new_start+1, len(outline_complete)+1):
            if half_height <= max(outline_complete[j], outline_complete[j+1]) and half_height >= min(outline_complete[j], outline_complete[j+1]) and np.positive(outline_complete[j]-outline_complete[j+1]) >= 80:
                m_segment = Calculate_M_Adjacent_Line(j, outline_complete[j], j+1, outline_complete[j+1])
                q_segment = Calculate_Q(m_segment, j, outline_complete[j+1])
                half_height_finish = (half_height - q_segment)/m_segment
    except Exception as e:
        print(e)
    print(k)
    print("hh s", half_height_start)
    print("hh f", half_height_finish)
    width_half_height_average.append(half_height_finish - half_height_start)
    
print("2° Method Results from Width at Half-Height")
print("Width Average", np.average(width_half_height_average), "px")
print("Delta Width", Get_Delta_Width(width_half_height_average), "px")
print("Standard Deviation", Get_Standard_Deviation(width_half_height_average), "px\n")

#this part of method plots the part of the outline near the cut
for k, v in outline_on_the_cut.items():
    plt.plot(v[0], 'o-', color='blue', markersize=4)
    mng = plt.get_current_fig_manager()
    mng.resize(1700, 700)
    mng.set_window_title(str(k))
    plt.show() 

#printing 2° method with results from lowest part of outline
print("2° Method Results from lowest part of outline")
print("Width Average", np.average(width_lowest_part_average), "px")
print("Delta Width", Get_Delta_Width(width_lowest_part_average), "px")
print("Standard Deviation", Get_Standard_Deviation(width_lowest_part_average), "px\n")

#this method plot the first profile and the last to see the difference
for k in outline_info.keys():
    try:
        plt.plot(outline_info[k][0], '*-', color='purple', markersize=6)
        plt.plot(outline_info[10][0], 'o-', color='blue', markersize=4)
        mng = plt.get_current_fig_manager()
        mng.resize(1700, 700)
        mng.set_window_title(str(k))
        #plt.show()
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