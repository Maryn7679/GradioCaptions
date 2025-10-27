import pandas as pd
from Functions.db_connection import default_app


def get_captions_by_video_id(video_id):
    response = default_app.database().child("Captions").child(video_id).get().val()
    captions = pd.DataFrame(response)
    captions_edit = captions[['start_time', 'text', 'end_time']]
    captions_edit.columns = ["Start", "Text", "End"]
    return captions_edit, captions


def save_dataframe(df, df_full, video_id, user):
    try:
        df_full["user_id"].loc[
            df_full["start_time"] != df["Start"] or
            df_full["end_time"] != df["End"] or
            df_full["text"] != df["Text"]
                                ] = user
        df_full["start_time"] = df["Start"].apply(lambda x: float(x))
        df_full["text"] = df["Text"]
        df_full["end_time"] = df["End"].apply(lambda x: float(x))

        df_json = df.to_json(orient="index")
        default_app.database().child("Captions").child(video_id).set(df_json)

        return "Save successful!"
    except ValueError:
        return "Save failed: Incorrect input format"
