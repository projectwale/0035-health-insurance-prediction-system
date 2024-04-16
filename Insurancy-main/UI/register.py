import face_recognition.api as face_recognition
import cv2, os, time, pickle
import numpy as np
# from mtcnn import MTCNN
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
# load image using cv2....and do processing.
import pymysql
import random
import traceback
def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="0035_health_insurance")
        return connection
    except:
        print("Something went wrong in database Connection")


def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

def register_yourself(name,Email, Phone, Password, Address):

    mpl.rcParams['toolbar'] = 'None'
    # PATH = "/home/harsh/Backup/face-recognition/data"
    PATH = "static/facedata/"
    STORAGE_PATH = "storage/"

    try:
        os.makedirs(PATH)
    except:
        pass

    try:
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"rb") as fp:
            known_face_ids = pickle.load(fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"rb") as fp:
            known_face_encodings = pickle.load(fp)
        # known_face_ids = np.load("known_face_ids.npy")
        # known_face_encodings = np.load("known_face_encodings.npy")
    except:
        known_face_encodings = []
        known_face_ids = []

    try:
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"r") as fp:
            id_idx = json.load(fp)
    except:
        id_idx = {}

    try:
        video_capture = cv2.VideoCapture(0)
        # usernamelist = input("Enter your id: ")
    
        IMAGE_PATH = os.path.join(PATH, name)
    
        try:
            os.makedirs(IMAGE_PATH)
        except:
            pass
    
        try:
            start = id_idx[name]
        except :
            start = 0
    
     
        i = 0
        j = start
    
        check, image = video_capture.read()
     
        while j < start + 10:   # Take 10 more images
    
            # if not video_capture.isOpened():
            #     print("ERROR OPENING CV")
            i += 1
            check, image = video_capture.read()
    
           
            if(i % 30 == 0):
                cv2.imwrite(IMAGE_PATH + "/{}_".format(name) + str(j) + ".jpg", image)
                try:
                    known_face_encodings.append(face_recognition.face_encodings(image)[0])
                    known_face_ids.append(name)
                except:
                    continue
                j += 1
                
                cv2.imshow('Capturing Images :',image)
                cv2.waitKey(2000)
                cv2.destroyWindow('Capturing Images :')
    
        with open( os.path.join(STORAGE_PATH, "known_face_ids.pickle"),"wb") as fp:
            pickle.dump(known_face_ids,fp)
        with open( os.path.join(STORAGE_PATH, "known_face_encodings.pickle"),"wb") as fp:
            pickle.dump(known_face_encodings,fp)
    
        id_idx[name] = start + 10
    
        video_capture.release()
        cv2.destroyAllWindows()
        # video_capture.
    
        with open( os.path.join(STORAGE_PATH, "id_idx.json"),"w") as outfile:
            json.dump(id_idx, outfile)
            
        all_image = os.listdir("static/facedata/"+str(name))
        single_image = random.choice(all_image)
        
        imagepath = "static/facedata/"+str(name)+"/"+str(single_image)
        
       
        con = dbConnection()
        cursor = con.cursor()
        sql="INSERT INTO registration(Name,Email,Phone,Password,Address,Profile_img) VALUES(%s,%s,%s,%s,%s,%s)"
        val = (name,Email, Phone, Password, Address,imagepath)
        print(sql)
        cursor.execute(sql,val)
        con.commit()
        dbClose()
        print("Register query submitted")
        return True
    except Exception as e:
        print('error',e)
        print(traceback.format_exc())
        return False
        
#register_yourself('ningesh')
