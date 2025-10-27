import gradio as gr
from Functions.video_player_functions import youtube_link_to_id, get_video_embed_by_id, get_video_link_by_pointer
from Functions.caption_editor_functions import get_captions_by_video_id, save_dataframe
from Resources.css import css

next_video_pointer = 0
user = ""


def get_username(profile: gr.OAuthProfile):
    global user
    user = profile.username
    return profile


def save(df, df_full, video_id):
    return save_dataframe(df, df_full, video_id, user)


def get_next_components():
    global next_video_pointer
    next_video_link = get_video_link_by_pointer(next_video_pointer)
    next_video_pointer += 1
    if next_video_link is None:
        next_video_link = get_video_link_by_pointer(0)
        next_video_pointer = 1

    next_video_id = youtube_link_to_id(next_video_link)

    next_video = get_video_embed_by_id(next_video_id)
    next_captions, next_captions_full = get_captions_by_video_id(next_video_id)

    return next_video, next_video_id, next_captions, next_captions_full


(start_video, start_video_id, start_captions, start_captions_full) = get_next_components()

with gr.Blocks(css=css) as main_page:
    gr.Markdown("# Caption Editor")

    gr.LoginButton()

    current_user = gr.Textbox(visible=False, interactive=False)
    current_video_id = gr.Textbox(value=start_video_id, visible=False, interactive=False)
    current_captions_full = gr.DataFrame(value=start_captions_full, visible=False, interactive=False)

    main_page.load(get_username, outputs=current_user)

    @gr.render(inputs=current_user)
    def render_page(logged_in_user):
        if logged_in_user is None:
            gr.Markdown("## Please log in via Hugging Face")
        else:
            with gr.Row():
                with gr.Column():
                    caption_editor = gr.DataFrame(interactive=True,
                                                  value=start_captions,
                                                  datatype=["number", "str", "number"],
                                                  row_count=(start_captions.shape[0], "fixed"),
                                                  col_count=(3, "fixed"), column_widths=["20%", "60%", "20%"])
                    save_button = gr.Button(value="Save")
                    save_result = gr.Markdown()
                with gr.Column():
                    video_embed = gr.HTML(value=start_video)
                    next_video_button = gr.Button("Next")

            next_video_button.click(fn=get_next_components,
                                    outputs=[video_embed, caption_editor, current_video_id, current_captions_full])
            save_button.click(fn=save,
                              inputs=[caption_editor, current_captions_full, current_video_id],
                              outputs=save_result)

main_page.launch(share=True, ssr_mode=False)
