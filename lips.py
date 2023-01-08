import cv2
import numpy as np
import dlib

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def imglips(saveFileName,img,savePath,BGR:tuple):
    #이미지 크기 반으로 축소
    img=cv2.resize(img,(0,0),None,0.8,0.8)
    imgOriginal=img.copy()
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=detector(imgGray)

    #faces가 0이 아니면 얼굴을 찾았다라는 걸로 함수 실행
    if len(faces)!=0:
        for face in faces:
            # x1,y1=face.left(),face.top()
            # x2,y2=face.right(),face.bottom()

            # imgOriginal=cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            landmarks=predictor(imgGray,face)

            myPoints=[]

            for n in range(68):
                x=landmarks.part(n).x
                y=landmarks.part(n).y
                myPoints.append([x,y])
                # cv2.circle(imgOriginal,(x,y),4,(50,50,255),cv2.FILLED)
                # cv2.putText(imgOriginal,str(n),(x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(0,0,255),1)

            myPoints=np.array(myPoints)
            
            # imgLeftEye=createBox(img,myPoints[17:21],3,masked=True,cropped=False)
            # imgLeftEyeColor=np.zeros_like(imgLeftEye)
            # imgLeftEyeColor[:]=BGR
            
            imgLips=createBox(img,myPoints[48:61],3,masked=True,cropped=False)

            imgClorLips=np.zeros_like(imgLips)
            
            imgClorLips[:]=BGR #B,G,R

            
            imgClorLips=cv2.bitwise_and(imgLips,imgClorLips)
            imgClorLips=cv2.GaussianBlur(imgClorLips,(7,7),10)
            imgClorLips=cv2.addWeighted(imgOriginal,1,imgClorLips,0.4,0.4)
            
            
            cv2.imwrite(f'{savePath}{saveFileName}',imgClorLips)
            return {
                'status':True,
                'fileLocation':fr'{savePath}{saveFileName}',
                'fileName':saveFileName
            }
    else:
        return {
            'status':False,
        }



def createBox(img,points,scale=5,masked=False,cropped=True):
    if masked:
        mask=np.zeros_like(img)
        mask=cv2.fillPoly(mask,[points],(255,255,255))
        # cv2.imshow('Mask',mask)
        img=cv2.bitwise_and(img,mask)
        # cv2.imshow('Mask',img)
        # cv2.waitKey(0)

    if cropped:
        bbox=cv2.boundingRect(points)
        x,y,w,h=bbox
        imgCrop=img[y:y+h,x:x+w]
        imgCrop=cv2.resize(imgCrop,(0,0),None,scale,scale)
        return imgCrop
    else:
        return mask