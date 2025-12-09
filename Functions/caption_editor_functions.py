import pandas as pd
from Functions.db_connection import default_app
from Resources.localization import get_string


def save_captions_to_db(df, video_id, user):
    try:
        data = df.copy()
        data.columns = ['start_time', 'text', 'end_time']
        df_json = data.to_dict(orient="index")
        default_app.database().child("video_captions").child(video_id).child("captions").set(df_json)
        default_app.database().child("video_captions").child(video_id).child("username").set(user)
        return get_string("save_successful")
    except Exception as e:
        return f"{get_string('save_failed')} {str(e)}"


def request_captions_by_video_id(video_id):
    response = default_app.database().child("video_captions").child(video_id).child("captions").get().val()
    if response is None:
        captions = pd.DataFrame(columns=["end_time", "start_time", "text"])
    else:
        captions = pd.DataFrame(response)
    captions_edit = captions[['start_time', 'text', 'end_time']]
    captions_edit.columns = ["Start", "Text", "End"]
    return captions_edit
