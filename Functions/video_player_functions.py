import re
from Functions.db_connection import videos_ref

def youtube_link_to_id(link):
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
    print(f"get_video_link_by_pointer: pointer = {pointer}")
    video_link_request = videos_ref.child(str(pointer)).get()
    video_link = video_link_request.val()
    print(f"get_video_link_by_pointer: videos_ref = {videos_ref}")
    print(f"get_video_link_by_pointer: videos_ref.child(str(pointer)) = {videos_ref.child(str(pointer))}")
    print(f"get_video_link_by_pointer: videos_ref.child(str(pointer)).get().val() = {videos_ref.child(str(pointer)).get().val()}")
    print(f"get_video_link_by_pointer: video_link = {video_link}")
    return video_link
