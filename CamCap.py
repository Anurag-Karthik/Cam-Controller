import cv2
import os

cam = cv2.VideoCapture(0)
signName = 'Pinch'
# I need Pinch, Three Finger Single and Double Flap while Pinch

if(not os.path.exists(f"O:/CamController/Data/Images/{signName}")):
    os.mkdir(f"O:/CamController/Data/Images/{signName}")
writtenCount = 0

while True:
    ret, img = cam.read()
    cv2.imshow('Camera', img)
    cv2.imwrite(f'O:/CamController/Data/Images/{signName}/{writtenCount}.jpg', img)
    print(f'Image Written at O:/CamController/Data/Images/{signName}/{writtenCount}.jpg')
    writtenCount = writtenCount + 1
    if cv2.waitKey(1) & 0xFF == ord('Q'):
        break

print(f"Written {writtenCount} Images")
cam.release()
cv2.destroyAllWindows()