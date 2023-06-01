import cv2

file_path = r"C:\Users\stage.upe4\Downloads\download.jpg"

image = cv2.imread(file_path)
print(image.shape)

image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
print(image_rotated.shape)
cv2.imwrite(file_path, image_rotated)