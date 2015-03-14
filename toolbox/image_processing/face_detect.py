""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')


while(True):  
# capture frame-by-frame
    ret, frame = cap.read()          
    faces = face_cascade.detectMultiScale(frame, scaleFactor = 1.2, minSize = (20,20))
    
    for (x,y,w,h) in faces:
        frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
        #rect= cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))  
        #eye balls
        cv2.circle(frame, ((x+(2*w/7)) ,(y+h/3)+10), 5, (255,255,255), thickness=25, lineType=8, shift=0) 
        cv2.circle(frame, ((x+(5*w/7)) ,(y+h/3)), 5, (255,255,255), thickness=25, lineType=8, shift=0) 
        
        #pupils
        cv2.circle(frame, ((x+(2*w/7)) ,(y+h/3)), 5, (0,0,0), thickness=8, lineType=8, shift=0) 
        cv2.circle(frame, ((x+(5*w/7)) ,(y+h/3)+10), 5, (0,0,0), thickness=8, lineType=8, shift=0) 

        cv2.imshow('frame' , frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# when everything is done, release the capture
cap.realease()
cv2.destroyAllWindows






# """ Experiment with face detection and image filtering using OpenCV """

# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)
# face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
# kernel = np.ones((21,21),'uint8')

# ret, frame = cap.read()
# faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
# for (x,y,w,h) in faces:
#     print "working"
#     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
#     # Display the resulting frame
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#        print "poop"

# cap.realease()
# cv2.destroyAllWindows

# raw_input("turd")






# """
# webcam-snapshot.py:
# A simple tool for taking snapshots from webcam. The images are saved in the 
# current directory named 1.jpg, 2.jpg, ...

# Usage:
#     Press [SPACE] to take snapshot
#     Press 'q' to quit
# """

# import cv2
# import sys
# cap = cv2.VideoCapture(0)
# def take_snapshot(delay=2):
#     #cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print "Cannot open camera!"
#     return

#     # Set video to 320x240
#     cap.set(3, 320) 
#     cap.set(4, 240)

#     take_picture = False;
#     t0, filenum = 0, 1

# while True:
#     val, frame = cap.read()
#     cv2.imshow("video", frame)
#     key = cv2.waitKey(30)
#     cv2.imwrite(str('name') + ".jpg", frame)
#     break

# if __name__ == "__main__":
#     take_snapshot()




