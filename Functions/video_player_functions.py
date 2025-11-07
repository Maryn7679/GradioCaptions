import urllib
from Functions.db_connection import default_app


def get_youtube_player_html():
    """Returns the static HTML container for YouTube player (API loaded in page head)"""
    return """
<div style="margin:0 auto; width: fit-content;">
  <div id="yt-container" style="width: 640px; height: 360px;"></div>
</div>
"""


def youtube_link_to_id(link):
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(link)
        return parse_qs(parsed.query)['v'][0]
    except (KeyError, IndexError):
        raise ValueError(f"Invalid YouTube URL: {link}")


def get_video_embed_by_id(video_id):
    """Returns just the video ID - actual loading happens via JavaScript in main_page"""
    return video_id


def get_video_link_by_pointer(pointer):
    video_link = default_app.database().child("Videos").child(str(pointer)).get().val()
    return video_link
