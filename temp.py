import gradio as gr


def get_youtube_player_html():
    """Returns the static HTML container for YouTube player (API loaded in page head)"""
    return """
<div style="margin:0 auto; width: fit-content;">
  <div id="yt-container" style="width: 640px; height: 360px;"></div>
</div>
"""


css = """
#yt-container {
}
"""

yt_init_js = """
<script src="https://www.youtube.com/iframe_api"></script>
<script>
window.onYouTubeIframeAPIReady = function() {
    window.ytPlayer = new YT.Player('yt-container', {
        height: '360',
        width: '640',
        playerVars: { 
            origin: window.location.origin, 
            playsinline: 1 
        },
        events: {
            'onReady': function(event) {
                window.ytPlayerReady = true;
            }
        }
    });
};
</script>
"""


with gr.Blocks(css=css, head=yt_init_js) as demo:
    video_embed = gr.HTML(value=get_youtube_player_html())
    current_video_id = gr.Textbox(value="tkMg8g8vVUo", visible=False, interactive=False)

    demo.load(
        fn=None,
        inputs=current_video_id,
        outputs=None,
        js="""(videoId) => {
            const checkPlayer = setInterval(() => {
                if (window.ytPlayer && window.ytPlayer.cueVideoById) {
                    clearInterval(checkPlayer);
                    window.ytPlayer.cueVideoById(videoId);
                }
            }, 100);
        }"""
    )

demo.launch()
