import cv2
import numpy as np
import flask

def Calculate_Thickness():
    cut_thickness = -1
    return cut_thickness

def Calculate_M_Adjacent_Ray(x1, y1, x2, y2):
    return (y2 - y1)/(x2 - x1)

def Calculate_M_Perpendicular_Ray(m1):
    return -1/m1
    

#imread method also need a flag, it can be 1, 0, -1 (color, grayscale, unchanged)
slab = cv2.imread(r"C:\Users\stage.upe4\Downloads\lastra_carta_routata.jpg")#reading an image from system

slab_grayscale = cv2.cvtColor(slab, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(slab_grayscale, 100, 255, cv2.THRESH_BINARY)

#fgbg = cv2.createBackgroundSubtractorMOG2()
#fgmask = fgbg.apply(thresh)


#y1SX = -1
#y1DX = -1
#for i in range(735):#the value in range method needs to be substituted with the value of the image
        #if fgmask[0, i] == 127 and fgmask[0, i+1] == 255:
            #y1SX = i
            #break
#for i in range(735):#the value in range method needs to be substituted with the value of the image
        #if fgmask[0, i] == 255 and fgmask[0, i+1] == 127:
            #y1DX = i+1
            #break

x1, y1, x2, y2 = 0, 0, 0, 0
width, height = thresh.shape
print(width)
print(height)

for i in range(height):
    if thresh[round((width/2)-30), i] == 255 and thresh[round((width/2)-30), i+1] == 0:
        x1 = i
        y1 = round((width/2)-30)
        break
for i in range(height):
    if thresh[round((width/2)+30), i] == 255 and thresh[round((width/2)+30), i+1] == 0:
        x2 = i
        y2 = round((width/2)+30)
        break
print(x1, y1, x2, y2)

back_to_rgb = cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB)
cv2.line(back_to_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)

if x1 != x2:
    m1 = Calculate_M_Adjacent_Ray(y1, x1, y2, x2)
    m2 = Calculate_M_Perpendicular_Ray(m1)
    print(m1, m2)
    cv2.line(back_to_rgb, (x1, round((width/2))), (x1+25, round((x1+25)*m2)), (0, 0, 255), 2)
else:
    cv2.line(back_to_rgb, (x1, round(width/2)), (x1+25, round(width/2)), (0, 0, 255), 2)

    
    
#TODO aggiungere la ricerca del punto a destra del taglio e se la il taglio è perpendicolare trovare lo spessore in modo facile nel caso in cui il taglio sia obliquo uso la formula del fascio di rette passanti per un punto e il coefficiente angolare è calcolato, trovo quindi la coordinata del punto che interseca la retta obliqua adiacente al taglio e poi ne calcolo lo spessore con il teorema di pitagora

#print(y1SX)
#print(y1DX)
#print("Spessore =" , y1DX-y1SX , "px")

#calculate the equation of the perpendicular ray to those ones
#image = Image.open(r"C:\Users\stage.upe4\Downloads\lastra_carta.jpg")
#print(image.info.get('dpi'))
#image.close()

#lower_gray = np.array([126, 126, 126])
#upper_gray = np.array([128, 128, 128])
#mask = cv2.inRange(fgmask, lower_gray, upper_gray)

#contours, hierarchy = cv2.findContours(slab_grayscale, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#for contour in contours:
    #image = cv2.drawContours(slab_grayscale, contour, -1, (0, 255, 0), 2)
    #contour_area = cv2.contourArea(contour)
    

#if the threshold and filter colors technique doesn't work it's worth trying to use HOG technique (Histogram of Oriented Gradients) 
#for i in range(980):
    #for j in range(735):
        #print(fgmask[i,j]) 
#print(contour_area)

cv2.imshow("Image", back_to_rgb)

cv2.waitKey(0)
cv2.destroyAllWindows()


#b = 124
#b = np.sqrt(b)
#print("Ciao")
#print(b)
