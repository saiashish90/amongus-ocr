import time
import numpy as np
import cv2
from pytesseract import image_to_data
from PIL import ImageGrab
from pytesseract import Output

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'amongus-44241'
})
db = firestore.client()

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
