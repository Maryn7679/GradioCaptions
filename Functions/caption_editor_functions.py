import pandas as pd
from Functions.db_connection import default_app


def get_captions_by_video_id(video_id):
    response = default_app.database().child("Captions").child(video_id).get().val()
    if response is None:
        captions = pd.DataFrame(columns=["clean_text", "end_time", "signer", "start_time", "text", "user_id"])
    else:
        captions = pd.DataFrame(response)
    captions_edit = captions[['start_time', 'text', 'end_time']]
    captions_edit.columns = ["Start", "Text", "End"]
    return captions_edit, captions


def save_dataframe(df, df_full, video_id, user):
    if len(df.index) > len(df_full.index):
        new_rows = len(df_full.index) - len(df.index)
        empty_data = {col: [None for _ in range(new_rows)] for col in df_full.columns}
        empty_df = pd.DataFrame(empty_data)

        df_full = pd.concat([df_full, empty_df], ignore_index=True)
    try:
        df_full["user_id"] = user
        df_full["start_time"] = df["Start"].apply(lambda x: float(x))
        df_full["text"] = df["Text"]
        df_full["end_time"] = df["End"].apply(lambda x: float(x))

        df_json = df_full.to_dict(orient="index")
        default_app.database().child("Captions").child(video_id).set(df_json)

        return "Save successful!"
    except ValueError:
        return "Save failed: Incorrect input format"
