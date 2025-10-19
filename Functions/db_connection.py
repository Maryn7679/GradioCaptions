import json

import firebase_admin
from firebase_admin import db
import os

# KEY_PATH = 'Resources/key.json'
key = os.getenv('FIREBASE_KEY')
key_json = json.loads(key)

cred_obj = firebase_admin.credentials.Certificate(key)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://video-link-db-default-rtdb.europe-west1.firebasedatabase.app/"
    })
videos_ref = db.reference("/Videos")
