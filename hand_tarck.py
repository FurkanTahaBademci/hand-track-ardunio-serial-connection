import serial
import cv2
import mediapipe
from datetime import time


print("[ INFO ] : SERİ BAĞLANTI KURULUYOR...")
ardunio = serial.Serial(port='COM8', baudrate=9600, timeout=0.1)
time.sleep(3)
print("[ INFO ] : SERİ BAĞLANTI KURULDU ")
print("[ INFO ] : KAMERA AÇILIYOR... ")
camera=cv2.VideoCapture(0)


mpHands=mediapipe.solutions.hands
hands= mpHands.Hands()
mpDraw=mediapipe.solutions.drawing_utils

font = cv2.FONT_HERSHEY_SIMPLEX
sonuc=0
bilgi = None
sart1 = 1
sart2 = 1
bilgi_yazi = " "


print("[ INFO ] : KAMERA AÇILDI ")

while True:

    success, img = camera.read()
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hlms = hands.process(imgRGB)
    height, width, channel = img.shape

    if hlms.multi_hand_landmarks:
        for handlandmarks in hlms.multi_hand_landmarks:

            for fingerNum, landmark in enumerate(handlandmarks.landmark):
                positionX, positionY = int(landmark.x * width), int(landmark.y * height)
       
                #------------EL HAREKETİ ALGILAMA ----------------#
                for i in range(8,21,4):
                    y1=handlandmarks.landmark[i].y
                    y=handlandmarks.landmark[i-3].y

                    if y1> y:
                        sonuc= sonuc+1 

                if sonuc>=4:
                    bilgi = 0

                if sonuc<4 :
                    x2,y2=handlandmarks.landmark[8].x, handlandmarks.landmark[8].y
                    x3,y3=handlandmarks.landmark[4].x, handlandmarks.landmark[4].y
                    if  -0.10<(y3-y2)<0.05:
                           bilgi = 1
                       

                sonuc=0
       
                #-----------  ARDUİNO BİLGİ ----------------#

                if bilgi == 0 and sart1 == 1:
                    bilgi_yazi = "LED KAPALI"
                   
                    
                    print("[ INFO ] : LED KAPALI ")
                    ardunio.write(b'0')
                    sart1 = 0
                    sart2 = 1


                if bilgi == 1 and sart2 ==1:

                    bilgi_yazi = "LED ACIK"
                    print("[ INFO ] : LED AÇIK ")
                    ardunio.write(b'1')
                    sart1 = 1
                    sart2 = 0


        mpDraw.draw_landmarks(img, handlandmarks,mpHands.HAND_CONNECTIONS) # ÇİZİM 

    cv2.putText(img,bilgi_yazi, (30,50),font,1,(0,0,255),2)

    cv2.imshow("CAMERA",img)

    if cv2.waitKey(1) & 0xFF == ord("q") or 0xFF == ord("Q"):
        print("[ INFO ] : KAMERA KAPATILDI ")
        # ardunio.write(b'0')
        break


