import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio
from pprint import pprint
import asyncio


async def pepe(doc):
    pprint((doc._reference.parent.parent.id))


def on_snapshot(doc_snapshot, changes, read_time):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(pepe(doc_snapshot[0]))
    loop.close()


cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'amongus-44241'
})
db = firestore.client()

watcher = db.collection('Mattt').document(str(692784786556583946)).collection(
    'amongus').document('stats').on_snapshot(on_snapshot)


async def main():
    await asyncio.sleep(30)
    print(watcher)
    watcher.unsubscribe()
    print("done")
    await asyncio.sleep(30)
asyncio.run(main())
