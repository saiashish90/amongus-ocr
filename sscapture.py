import time
import cv2
import pytesseract
import numpy as np
from mss import mss
from pytesseract import Output

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

key = {
    "type": "service_account",
    "project_id": "amongus-44241",
    "private_key_id": "016a62c3b3bb3d546f922a2d68c9d93d07ce49f0",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDTM8cI9vAvuA7E\nwIT9WuASMtW4mVfpaHAz/vvcn1vLX0sqjEZkO5a/JrljPZiLMD2yBFrurXcXMQUX\nH9h8WgDHW0SSTyeO5deF9sk+ds1q4cXeJLhzQWa0iXvMIHSZD6NqH3tPNPzZNsPK\nFGxFHNN2zaQI9KtxR8/EQ2iJ3ibXeF57nIYUlFWpGkskruzsJnBJgRO8K51C6Wqp\nMakspP0L1plz2PwMnYobOFxYKUOyyinly0+HbC8MnTSD8433XqmFXY2MVJJGAI4t\nx57Ya1rD7p/cMfb81sJYFMYizN6ruRw0Elua/FrY0T4i4j2l7o077Wa5ANrENTw9\nRILbg8UDAgMBAAECggEAIKP5aDzFvRI8khLQ2tj/FUDu/9MPH58I7DhFk4C7bpBh\nLQe130rITu18rEY6O5SujEMZDJcZdyeXyk2dJwa/5Q+JZvU9v1ttNiKAUpuIvrJ6\n4oyZRxK9/TvcOp1vd7JPhpir9X9Sbn2Ev8ftPbcpRUydw9aQYnb/OK1UTC5doWIM\nccNl1msOx3pTr0EoKkmuGbNoasdTiVAwjdI/ELCG+yhLctaBAj9aifY2KNNnQj0p\nSGwkcoqhqnoRNRrdSkJH+Wljzn8gxxbWwTNod9Q8xjVE5FCx8oq+FIZElr+UmV+L\n15sRtjJMMWOhB/PDDJP7poZDi9wEOg9ykRUXJv6SsQKBgQD3TGGMxpk644PQRHUp\nBu+v87UuTqVvHxc2c55JsQT7nB7nFiR8e+nEEvYQT18K6sGd7AnajPcAFWYxn+Sy\nKEgIU9ZkEfxZPnlJQjUNYxLk2wmd63AVhtKU05UOseMv6U1ZHrcdn5VokVx6DRGc\ndJcvAyFvsl+jJb7b3Bbp9d1aMQKBgQDaoj/MgkpjT5ABY3VkN6pgJ0CAG3/61yFh\nxH/ZypHfWR1TYODY+E8OpxHHNk8aplS2jLHtud1tA3rokzNoxAQcE6F+R3Rik4zV\nbiPiPp6YwMThWI95rMuoymn6Hd3og7Wfl9rF15y44xSB3+71us/2hHkPef8zclcR\n5jkNuscRcwKBgF6AXbbCHcQXNUPdJThsYiPG6bGsdCOmqeQxAof+kXzlCBoeqAq5\n/3biGA3bhuJRG3QRwyI1RB5QDyFfjLFYG06zWvYauWgRK6AHIObguVOjMGWcltRj\nFQ2yXP+kksC4Usp/plI3rYysH760R8qV80AP3jMk4s8hmXHDBS6aud/BAoGBAK8F\nk+0zoDlASBfUdvVzWoD+6zOi0CEOdzq9A1xmPcB+pmtI8ra+kQs505GWeFztKoO4\nvfeBAzFxx8LHlDAaOu//BxkAOrtvQx7YvQEw/+Vo7DM5oiHVonPNFmmT30FzrsHD\n3u7iXCPmJVSS38j3c+P0yLULBLE6p1k85A+JpjLhAoGABprex5OBPhFXV1JsPd86\ndxETOYYjJtt4nOcE2Yo8ZfqA/CDahzTJ1qPfvZhDkVuuYEPiMgqfLJG+QFSTtiEP\n5RShR4DbqEnltdJ2/XqXuRBNHkRC+Axa0kiKmeBtgSSOmjk9wBlYD+NDPj6taHCA\nksCS9Jd6Wlat3pOlAIxS/Ds=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ebkp7@amongus-44241.iam.gserviceaccount.com",
    "client_id": "117963512703673436185",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ebkp7%40amongus-44241.iam.gserviceaccount.com"
}

cred = credentials.Certificate(key)
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
    with mss() as sct:
        name = name + '.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        desired_fps = 1.0
        out = cv2.VideoWriter(name, fourcc, desired_fps,
                              (mon['width'], mon['height']), 0)
        last_time = 0
        status = 'discussion'
        while True:
            img = np.array(sct.grab(mon))
            img[:, :, 1] = np.zeros([img.shape[0], img.shape[1]])
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            if time.time() - last_time > 1./desired_fps:
                d = pytesseract.image_to_data(img, output_type=Output.DICT)
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
