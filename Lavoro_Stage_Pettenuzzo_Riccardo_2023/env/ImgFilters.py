import cv2

file_path = r"C:\Users\stage.upe4\Downloads\lastra_vera_cropped.jpg"

image = cv2.imread(file_path)
image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_grayscale_blur_m = cv2.medianBlur(image_grayscale, 15)
image_grayscale_blur_g = cv2.GaussianBlur(image_grayscale, (19, 19), 0)

fgbg = cv2.createBackgroundSubtractorMOG2()
#fgmask = fgbg.apply(thresh)

ret, thresh4 = cv2.threshold(image_grayscale_blur_m, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret, thresh3 = cv2.threshold(image_grayscale_blur_g, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#this method avoid choosing the threshold value and it choose it automatically thank to an histogram that represent the bi-color image

thresh1 = cv2.adaptiveThreshold(image_grayscale_blur_g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 55)
thresh2 = cv2.adaptiveThreshold(image_grayscale_blur_m, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 55)
#this method is not choosing a static value as threshold but it chooses a value for a small region of image 
#this method can may have a problem with the middle of the cut but with background remove there'll may be a solution

thresh5 = cv2.adaptiveThreshold(image_grayscale_blur_g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 55)
thresh6 = cv2.adaptiveThreshold(image_grayscale_blur_m, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 55)


cv2.imshow("OTSU and Gauss Blur", thresh3)
cv2.imshow("Adaptive Gauss and Gauss Blur", thresh1)
cv2.imshow("OTSU and Median Blur", thresh4)
cv2.imshow("Adaptive Gauss and Median Blur", thresh2)
cv2.imshow("Adaptive Mean and Gauss Blur", thresh6)
cv2.imshow("Adaptive Mean and Median Blur", thresh5)

cv2.waitKey(0)
cv2.destroyAllWindows()