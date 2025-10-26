import firebase

firebaseConfig = {
                  "apiKey": "AIzaSyBVTnll2fdV3qkQ4EFG3hsRMO6P4phW7Kc",
                  "authDomain": "video-link-db.firebaseapp.com",
                  "databaseURL": "https://video-link-db-default-rtdb.europe-west1.firebasedatabase.app",
                  "projectId": "video-link-db",
                  "storageBucket": "video-link-db.firebasestorage.app",
                  "messagingSenderId": "777912710342",
                  "appId": "1:777912710342:web:9ac9387604fc35262953c7"
}

default_app = firebase.initialize_app(firebaseConfig)
db = default_app.database()
videos_ref = db.child("Videos")