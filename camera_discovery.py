import cv2
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

cap = cv2.VideoCapture(os.environ["TV_TESTER_CAMERA"], cv2.CAP_FFMPEG)
# tive que tentar varias vezes, funcionou na rede frensch_3
# tive que habilitar o rtsp no app da yoosee e a senha também
# o usuário é sempre admin
while True:
    ret, image = cap.read()
    cv2.imshow("Test", image)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()