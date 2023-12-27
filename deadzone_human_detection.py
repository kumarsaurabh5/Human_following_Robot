import mediapipe as mp
import cv2
import math
import serial

def slope(p2, p1):
    a = (p2[1] - p1[1])
    b = (p2[0] - p1[0])
    if (b != 0):
        slao = a / b
        return slao
    else:
        return 0
# ser = serial.Serial('com3',9600)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0)

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
#ser = serial.Serial('COM4',9600)
# x1=0
# y1=0
direction = "" 
deadzoneleft = 240
deadzoneright = 400
deadonetop=120

print('EXECOYERT')
while True:
    
    ret,image = cap.read()
    image = cv2.flip(image,1)
    cv2.line(image,(320,0),(320,480),(0,0,255),2)
    cv2.line(image,(0,240),(640,240),(0,0,255),2)
    
                                                      
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    h, w, c = image.shape
    xc= w/2
    yc= h/2

    if (results.pose_landmarks):

        x1= results.pose_landmarks.landmark[24].x * w

        y1 = results.pose_landmarks.landmark[24].y * h

        x2= results.pose_landmarks.landmark[23].x * w
        y2 = results.pose_landmarks.landmark[23].y * h


        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        xh = int((x1+x2)/2)
        yh = int((y1+y2)/2)

        if xh<deadzoneleft:
            direction = "L"
        elif xh>deadzoneright:
            direction = "R"
        else:
            direction = "S"

        # ser.write(direction.encode())
    image = cv2.putText(image,direction,(30,30), cv2.FONT_HERSHEY_SIMPLEX,
                   1,(0,255,0), 1, cv2.LINE_AA)


        
        


    cv2.imshow("q",image)

    if(cv2.waitKey(1)==ord('q')):

        break