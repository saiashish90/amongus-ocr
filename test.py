import time
import numpy as np
import cv2
from pytesseract import image_to_string
from PIL import ImageGrab
from pytesseract import Output

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def processDiscussion(image: complex) -> int:
    #1 = Not found, 2 = Discussion found, 3 = Voting ended found

    discussion = {"?","impestoe","who",'whos',"wino","innoosttor?","imsoster?","inostor?","imposter?","inyoostor?","iniposior?","inijposior?","impostor?","inoster?","tnrpester?","tnsester?","inraostor?","inaoster?","tnsoster?","tnpester?",'hnnsester?'}
    voting = {"voting", "results","result","vetting","vartine","votingiresults","vetting)","\\n\\nvatiing","results\\n\\n","resulis\\n\\n","resuilis\\n\\n","resulis","resuilis"}
    raw_output = image_to_string(image)
    
    out = set(raw_output.strip().strip('\n').strip("\\").strip("/").lower().split(" "))

    if len(out.intersection(discussion)) != 0: #if one of the keywords for discussion time is present
        print("DISCUSSION [UNMUTED]")
        return 2

    elif len(out.intersection(voting)) != 0: #if one of the keywords for ended voting is present
        print("VOTING ENDED [MUTING SOON]")

        return 3
    else:
        return 1

def processEnding(image: complex) -> bool:
    delay = 3.5 #Delay between getting role and game starting
    defeat = {"defeat","deteat","netrtorat","neffeat","netfeat","defeat\\n\\n"}
    victory = {"victory","vicory","viton"}
    imposter = {"imposter","impostor","tmonetor"}
    crewmate = {"crewmate"} 
    lobby = {'code'}   
    raw_output = pytesseract.image_to_string(image)
    out = set(raw_output.strip().strip('\n').strip("\\").strip("/").lower().split(" "))

    if len(out.intersection(defeat)) != 0: 
        print("DEFEAT [UNMUTED]")
        return True

    elif len(out.intersection(victory)) != 0: 
        print("VICTORY [UNMUTED]") 
        return True

    elif len(out.intersection(crewmate)) != 0: 
        print("YOU GOT CREWMATE [MUTING SOON]")
        time.sleep(delay + delay_start) #mute
        return False

    elif len(out.intersection(imposter)) != 0: #
        print("YOU GOT IMPOSTER [MUTING SOON]")
        time.sleep(delay + delay_start) 
        return False
    else:
        print(".")
        return True

def record(name):
    name = name + '.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    desired_fps = 1.0
    out = cv2.VideoWriter(name, fourcc, desired_fps,
                          (1920, 1080), 0)
    last_time = 0
    status = 'discussion'
    while True:
        if time.time() - last_time > 1./desired_fps:
            img = np.array(ImageGrab.grab(bbox=(0,0,1920,1080)))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            lobbyEnded = processEnding(img)
            if lobbyEnded:
                print("In lobby")
            cv2.putText(img, status, (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


record("Video")
