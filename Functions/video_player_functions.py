import re
# from Functions.db_connection import videos_ref
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

def youtube_link_to_id(link):
    print(f"youtube_link_to_id video link: {link}")
    video_id = re.findall("=(.*?)&", link)
    if len(video_id) == 0:
        video_id = re.findall("=(.*)", link)
    return video_id[0]


def get_video_embed_by_id(video_id):
    return f"""
    <div class="container">
    <iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen class="video"></iframe>
    </div>"""


def get_video_link_by_pointer(pointer):
    video_link = videos_ref.child(str(pointer)).get().val()
    print(f"get_video_link_by_pointer video link {video_link}")
    return video_link
