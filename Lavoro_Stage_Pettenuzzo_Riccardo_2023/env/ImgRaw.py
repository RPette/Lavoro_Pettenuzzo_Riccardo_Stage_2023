import rawpy
import cv2

stringa="C:\\Users\\stage.upe4\\Downloads\\raw\\IMG_0001_1.cr2"

print(stringa.split(".")[-1])#split the path and take only the file type 
raw = rawpy.imread(stringa) # access to the RAW image
rgb = raw.postprocess() # a numpy RGB array
image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR) # the OpenCV image