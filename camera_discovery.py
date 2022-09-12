import cv2
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

cap = cv2.VideoCapture("rtsp://admin:brewedattheeagle1@192.168.0.44:554/onvif1", cv2.CAP_FFMPEG)
#tive q tentar varias vezes, funcionou na rede frensch_3
# tiver q habilitar o rtsp no app da yoosee e a senha também
# o usuário é sempre admin
while True:
    ret, image = cap.read()
    cv2.imshow("Test", image)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()