import mediapipe as mp
import cv2
import math
import serial

# ser= serial.Serial ('COM4',9600)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0)

pose = mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)

while True:
    
    ret,image = cap.read()
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
        global x1 
        x1= results.pose_landmarks.landmark[0].x * w
        global y1
        y1 = results.pose_landmarks.landmark[0].y * h

        x1 = int(x1)
        y1 = int(y1)
        cv2.line(image,(x1,y1),(320,240),(255,0,255),2)

        cv2.circle(image,(x1,y1),20,(0,0,255),-1)

    
        k = w/2 + 120
        point = [[x1,y1],[w/2,h/2],[k,h/2]]
        def slope(p2,p1):
          a = (p2[1]-p1[1])
          b =(p2[0]-p1[0]) 
          if(b!=0):
           slao = a/b 
           return slao
          else: 
            return 0

        def angle():
        
            a = point[0]
            b = point [1]
            c = point [2]
    
            m1 = slope(b,a)
            m2 = slope (b,c)
            angle = math.atan((m2-m1)/(1+m1*m2))
            angle = round(math.degrees(angle))
            if angle <0:
                 angle = 180+ angle
            #cv2.putText(image, str((angle)), (50,50), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255),2,cv2.LINE_AA)
            
            # print(angle)
            return angle

        angle()  

      
      
      
      
        global direction
        i = 0
        while i< 6:
           if((xc-x1)>0 and (yc-y1)>0):
               angle1 = angle()-95
               z= int(angle1/15)
               print(z)
               if( z<=2):
                direction = 'F'
               # elif(z==2):
               #  direction = 'L'
               elif(z ==3):
                  direction = 'W'
               elif(z==4): 
                  direction = 'X'
               elif(z==5):
                     direction = 'Y'
               elif (z==6): 
                     direction = 'Z'



           #move   anticlockwise and forward


           elif((xc-x1)<0 and (yc-y1)>0):
               angle1= 85-angle()
               
               z= int(angle1/15)
               print(z)
               if( z<=2):
                direction = 'F'
               # elif(z==2):
               #    direction = 'V'
               elif(z ==3):

                   
                  direction = 'M'
               elif(z==4): 
                  direction = 'N'
               elif(z==5):
                     direction = 'O'
               elif (z==6): 
                     direction = 'P'
           #move clockwise and forward

           elif((xc-x1)>0 and (yc-y1)<0):
               angle1=angle()-40
               z= int(angle1/15)
               print(z)
               # if( z<=2):
               direction = 'F'
               # elif(z ==3):
               #    direction = 'M'
               # elif(z==4): 
               #    direction = 'N'
               # elif(z==5):
               #       direction = 'O'
               # elif (z==6): 
               #       direction = 'P'

        

        
        #move anticlockwise and backward
            
           elif((xc-x1)<0 and (yc-y1)<0):
               angle1=140-angle()
               z= int(angle1/15)
               print(z) 
               # if( z<=2):
               direction = 'F'
               # elif(z ==3):
               #     direction = 'W'
               # elif(z==4): 
               #     direction = 'X'
               # elif(z==5):
               #        direction = 'Y'
               # elif (z==6): 
               #        direction = 'Z'
           i=i+1   
           print(direction)
          # cv2.putText(image, str((direction)), (50,50), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255),2,cv2.LINE_AA)
        # ser.write(direction.encode())
       
        
    else:
      direction = 'S'
      print(direction)
      # ser.write(direction.encode())
   
        


    cv2.imshow("q",image)

    if(cv2.waitKey(1)==ord('q')):

        break