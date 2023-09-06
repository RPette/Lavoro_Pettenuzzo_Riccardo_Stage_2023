import cv2

#define the camera that would be used using an index 
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

#define variable for the codec
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3856)#widht of the image
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2764)#heigth of the image
cap.set(cv2.CAP_PROP_FORMAT, -1)#format of the video/photo
cap.set(cv2.CAP_PROP_FPS, 7)#fps of the camera 
cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)#if something needs to be converted to rgb
cap.set(cv2.CAP_PROP_FOURCC, fourcc)#define the codec


result, image = cap.read()#read a frame from the camera
cv2.imshow('image', image)

cv2.waitKey(0)
cap.release()#after reading a frame it releases the camera
cv2.destroyAllWindows()