import cv2

file_path = r"C:\Users\stage.upe4\Downloads\download.jpg"

image = cv2.imread(file_path)

image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

cv2.imwrite(file_path, image_rotated)