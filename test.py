import json
import requests
from google.oauth2.credentials import Credentials
from google.cloud.firestore import Client
import asyncio
from pprint import pprint

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
pprint(user)
cred = Credentials(user['idToken'], user['refreshToken'])
db = Client('amongus-44241', cred)
watcher = db.collection('Mattt').document(
    str(692784786556583946)).collection('amongus').document('stats').get().to_dict()
pprint((watcher))
db.collection('Mattt').document(str(692784786556583946)).collection('amongus').document('stats').update({
    "game_state": "ok",
})
watcher = db.collection('Mattt').document(
    str(692784786556583946)).collection('amongus').document('stats').get().to_dict()
pprint((watcher))
# async def main():
#     await asyncio.sleep(30)
#     print(watcher)
#     watcher.unsubscribe()
#     print("done")
#     await asyncio.sleep(30)
# asyncio.run(main())
