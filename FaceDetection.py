import cognitive_face as CF 
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import cv2
import time
import os



def getRectangle(faceDictionary):
    # print(faceDictionary[0]['faceRectangle'])
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    # print(str((left, top), (bottom, right)))
    return left, top,bottom, right

def getFacialFeatures(faceDictionary):
    attr = faceDictionary['faceAttributes']
    age = attr['age']
    gender = attr['gender']
    facialHair = attr['facialHair']
    return age,gender,facialHair


# Replace with a valid subscription key (keeping the quotes in place).
KEY = '[your microsoft face cognitive service key here]'
CF.Key.set(KEY)

# Replace with your regional Base URL
BASE_URL = 'https://portalfacedetection.cognitiveservices.azure.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
# img_url = 'https://images.pexels.com/photos/428364/pexels-photo-428364.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
# faces = CF.face.detect(img_url)
# print(faces)
cap = cv2.VideoCapture(0)



if not os.path.exists("images"):
    os.makedirs("images")
count=0
while True: 
    count +=1
    ret, frame = cap.read()
    temp_img = "images/temp-img%d.png"%count
    cv2.imwrite(temp_img,frame)
    faces = CF.face.detect(temp_img, attributes= 'gender,age,facialHair')
    img = cv2.imread(temp_img)
    # cv2.imshow('jgj',img)
    # time.sleep(2)
    if len(faces)>0:
        print(faces)
        for i in range(0,len(faces),1):
            x,y,width,height = getRectangle(faces[i])
            cv2.rectangle(img, (x,y), (width,height),(0xFF, 0xFF, 0), 2)
            age,gender,facialHair = getFacialFeatures(faces[i])
            overlay_text = '%s %s \n%s' % (gender, age, facialHair)
            cv2.putText(img, overlay_text,(x, y-20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0xFF, 0xFF, 0xFF), 2, cv2.LINE_AA)
        cv2.imshow("sdjvsc",img)

    if cv2.waitKey(5) == 27:  # ESC key press
        break

cap.release()
cv2.destroyAllWindows()

# Download the image from the url
# response = requests.get(img_url)
# img = Image.open(BytesIO(response.content))

# # For each face returned use the face rectangle and draw a red box.
# draw = ImageDraw.Draw(img)
# for face in faces:
#     draw.rectangle(getRectangle(face), outline='red')

# # Display the image in the users default image browser.
# img.show()