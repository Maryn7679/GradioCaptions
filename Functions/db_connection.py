import firebase
import json
import os

firebaseConfig = os.getenv("FIREBASE_CONFIG")
config_json = json.loads(firebaseConfig)

default_app = firebase.initialize_app(config_json)
