import time
import numpy as np
import cv2
from pytesseract import image_to_data
from PIL import ImageGrab
from pytesseract import Output

import json
import requests
from google.oauth2.credentials import Credentials
from google.cloud.firestore import Client

FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"


def sign_in_with_email_and_password(api_key, email, password):
    request_url = "%s:signInWithPassword?key=%s" % (FIREBASE_REST_API, api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password,
                       "returnSecureToken": True})

    req = requests.post(request_url, headers=headers, data=data)
    return req.json()


user = sign_in_with_email_and_password(
    'AIzaSyChb8Ebkbny-DLRYkqzi8feF7ej5tBLDyA', 'saiashish60@gmail.com', 'qwertyuiop')
cred = Credentials(user['idToken'], user['refreshToken'])
db = Client('amongus-44241', cred)

print("Enter game code")
code = str(input())
guild = None
guild_ids = db.collection('Mattt').get()
for guild_id in guild_ids:
    if code == (guild_id._reference.collection('amongus').document('stats').get().to_dict()['game_code']):
        guild = guild_id.id
        break
    else:
        print("Pls use the $amongus command first before loading this application")
mon = {'top': 0, 'left': 0, 'width': 310, 'height': 100}


def record(name):
    name = name + '.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    desired_fps = 1.0
    out = cv2.VideoWriter(name, fourcc, desired_fps,
                          (mon['width'], mon['height']), 0)
    last_time = 0
    status = 'discussion'
    while True:
        if time.time() - last_time > 1./desired_fps:
            img = np.array(ImageGrab.grab(bbox=(0,0,310,100)))
            img[:, :, 1] = np.zeros([img.shape[0], img.shape[1]])
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            d = image_to_data(img, output_type=Output.DICT)
            if 'TASKS' in d['text'] and 'COMPLETE' in d['text']:
                if status != 'tasks':
                    status = "tasks"
                    print('tasks', d['text'])
                    db.collection('Mattt').document(str(guild)).collection('amongus').document('stats').update({
                        "game_state": status,
                    })
            else:
                if status != 'discussion':
                    print("discussion", d['text'])
                    status = "discussion"
                    db.collection('Mattt').document(str(guild)).collection('amongus').document('stats').update({
                        "game_state": status,
                    })
            last_time = time.time()
            cv2.putText(img, status, (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


record("Video")
