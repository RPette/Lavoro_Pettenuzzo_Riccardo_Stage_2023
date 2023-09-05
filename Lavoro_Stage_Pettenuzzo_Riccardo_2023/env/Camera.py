import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3856)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2764)

available_backends = [cv2.videoio_registry.getBackendName(i) for i in cv2.videoio_registry.getBackends()]

fourcc = cv2.VideoWriter_fourcc(*'MJPG')

cap.set(cv2.CAP_PROP_FOURCC, fourcc)

cap.set(cv2.CAP_PROP_FORMAT, -1)

cap.set(cv2.CAP_PROP_FPS, 7)

cap.set(cv2.CAP_PROP_CONVERT_RGB, 1)

result, image = cap.read()

cv2.imshow('image', image)

cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()