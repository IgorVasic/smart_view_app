import numpy as np
import cv2
from openalpr import Alpr

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("md")


cap = cv2.VideoCapture("rtsp://admin:Admin1234@10.8.0.7:5544")
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

ret, frame = cap.read()
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

while(True):
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    results = alpr.recognize_ndarray(gray)
    print(results['results'])

cv2.destroyAllWindows()
alpr.unload()
cap.release()