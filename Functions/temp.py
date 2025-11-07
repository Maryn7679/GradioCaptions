import urllib


def youtube_link_to_id(link):
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(link)
        return parse_qs(parsed.query)['v'][0]
    except (KeyError, IndexError):
        raise ValueError(f"Invalid YouTube URL: {link}")


print(youtube_link_to_id("https://www.youtube.com/watch?v=tkMg8g8vVUo&ab_channel=ASLTHAT"))
