import gradio as gr
import pandas as pd
from Functions.video_player_functions import youtube_link_to_id, get_video_link_by_pointer, get_youtube_player_html, change_video_completion_status
from Functions.caption_editor_functions import request_captions_by_video_id, save_captions_to_db
from Resources.css import css
from Resources.js import yt_init_js
from Resources.localization import get_string

next_video_pointer = 0
user = "anonymous_user"
n_videos = 21
placeholder_link = "https://www.youtube.com/watch?v=1pXUgdCnVec"


def get_username(profile: gr.OAuthProfile):
    global user
    if profile is None:
        user = "anonymous_user"
    else:
        user = profile.username
    return profile


def on_row_select(df, evt: gr.SelectData):
    """Handle row selection in DataFrame"""
    if evt.index is not None and len(evt.index) > 0:
        row_idx = evt.index[0]
        if row_idx < len(df):
            row = df.iloc[row_idx]
            return (
                gr.update(visible=True),  # editing_panel
                gr.update(value=float(row['Start'])),  # start_time
                gr.update(value=str(row['Text'])),  # text_input
                gr.update(value=float(row['End'])),  # end_time
                gr.update(value=row_idx),  # selected_row_idx
                gr.update(value=get_string("update_entry_button"))  # save_entry_button
            )
    return gr.update(visible=False), "", "", "", -1, get_string("save_entry_button")


def show_add_entry_form():
    """Show editing panel for adding new entry"""
    return (
        gr.update(visible=True),  # editing_panel
        gr.update(value=0.0),  # start_time
        gr.update(value=""),  # text_input
        gr.update(value=0.0),  # end_time
        gr.update(value=-1),  # selected_row_idx (-1 means new entry)
        gr.update(value=get_string("add_entry_button_form"))  # save_entry_button
    )


def save_entry(df, start_time, text, end_time, selected_row_idx, video_id):
    """Save or update a caption entry"""
    if user == "anonymous_user":
        return df, gr.update(visible=True), gr.Warning(get_string("please_sign_in"))
    if next_video_pointer == -1:
        return df, gr.update(visible=True), gr.Success(get_string("all_videos_transcribed"))
    try:
        start_time = float(start_time)
        end_time = float(end_time)

        if start_time >= end_time:
            return df, gr.update(visible=True), gr.Warning(get_string("start_less_than_end"))

        if not text.strip():
            return df, gr.update(visible=True), gr.Warning(get_string("text_cannot_be_empty"))

        df_copy = df.copy()

        if selected_row_idx == -1:  # Adding new entry
            new_row = pd.DataFrame({
                'Start': [start_time],
                'Text': [text.strip()],
                'End': [end_time]
            })
            df_copy = pd.concat([df_copy, new_row], ignore_index=True)
            # Sort by start time
            df_copy = df_copy.sort_values('Start').reset_index(drop=True)
        else:  # Updating existing entry
            if 0 <= selected_row_idx < len(df_copy):
                df_copy.iloc[selected_row_idx] = [start_time, text.strip(), end_time]
                # Sort by start time
                df_copy = df_copy.sort_values('Start').reset_index(drop=True)

        # Update in database
        save_result = save_captions_to_db(df_copy, video_id, user)

        return (
            df_copy,
            gr.update(visible=False),  # Hide panel on success
            gr.Info(f"{save_result}")
        )

    except ValueError as e:
        return df, gr.update(visible=True), gr.Warning(f"{get_string('invalid_time_format')} {str(e)}")
    except Exception as e:
        return df, gr.update(visible=True), gr.Error(f"{get_string('error')} {str(e)}")


def cancel_edit():
    """Cancel editing and hide the form"""
    return gr.update(visible=False)


def change_completion_status(completion_status):
    global next_video_pointer
    change_video_completion_status(completion_status, (next_video_pointer + n_videos - 1) % n_videos)


def get_next_components():
    global next_video_pointer
    if next_video_pointer != -1:
        next_video_link = get_video_link_by_pointer(next_video_pointer)
        next_video_pointer = (next_video_pointer + 1) % n_videos

        for i in range(n_videos + 1):
            if next_video_link is not None:
                break
            next_video_link = get_video_link_by_pointer(next_video_pointer)
            next_video_pointer = (next_video_pointer + 1) % n_videos
        if next_video_link is None:
            next_video_link = placeholder_link
            next_video_pointer = -1

    try:
        next_video_id = youtube_link_to_id(next_video_link)
        next_captions = request_captions_by_video_id(next_video_id)
        return next_captions, next_video_id
    except (ValueError, Exception) as e:
        empty_captions = pd.DataFrame(columns=["Start", "Text", "End"])
        return empty_captions, "error"


(start_captions, start_video_id) = get_next_components()

with gr.Blocks(css=css, head=yt_init_js, fill_width=True) as main_page:
    user_state = gr.State("anonymous_user")
    pointer_state = gr.State(0)

    current_video_id = gr.Textbox(value="", visible=False, interactive=False)
    selected_row_idx = gr.Number(value=-1, visible=False)

    main_page.load(get_username, outputs=user_state)

    with gr.Row(variant="panel"):
        with gr.Column(scale=4):
            gr.Markdown(f"## {get_string('app_title')}")
        with gr.Column(scale=4):
            @gr.render(inputs=user_state)
            def check_login(logged_in_user):
                if logged_in_user == "anonymous_user":
                    gr.Markdown(get_string("please_log_in"), rtl=True)
                else:
                    gr.Markdown(f"{get_string('logged_in_as')} {logged_in_user.username}", rtl=True)
        with gr.Column(scale=1, min_width=50):
            gr.LoginButton(value=get_string("log_in_button"), logout_value=get_string("log_in_button"))

    with gr.Row():
        with gr.Column(scale=2, min_width=600):
            video_embed = gr.HTML(value=get_youtube_player_html())
            next_video_button = gr.Button(get_string("next_button"), key="next_video")
        with gr.Column(scale=1, min_width=200):
            caption_editor = gr.DataFrame(
                interactive=False,
                elem_id="tbl",
                datatype=["number", "str", "number"],
                col_count=(3, "fixed"),
                column_widths=["20%", "60%", "20%"],
                headers=[get_string("header_start"), get_string("header_text"), get_string("header_end")],
                wrap=True
            )
            add_entry_button = gr.Button(get_string("add_entry_button"), variant="secondary")
            editing_complete_checkbox = gr.Checkbox(label=get_string("editing_complete_checkbox"))

    with gr.Row():
        with gr.Group(visible=False) as editing_panel:
            gr.Markdown(f"### {get_string('edit_caption_title')}")
            with gr.Row(equal_height=False):
                with gr.Column():
                    start_time_input = gr.Textbox(label=get_string("start_time_label"), value="0.000", interactive=False)
                    insert_start_time_button = gr.Button(get_string("insert_current_time"))
                with gr.Column():
                    text_input = gr.Textbox(label=get_string("caption_text_label"), placeholder=get_string("caption_text_placeholder"))
                with gr.Column():
                    end_time_input = gr.Textbox(label=get_string("end_time_label"), value="0.000", interactive=False)
                    insert_end_time_button = gr.Button(get_string("insert_current_time"))

            with gr.Row(equal_height=False):
                save_entry_button = gr.Button(get_string("save_entry_button"), variant="primary")
                cancel_button = gr.Button(get_string("cancel_button"), variant="secondary")

    save_result = gr.Markdown()

    main_page.load(
        fn=get_next_components,
        outputs=[caption_editor, current_video_id],
        js="""() => {
            const checkPlayer = setInterval(() => {
                if (window.ytPlayer && window.ytPlayer.cueVideoById) {
                    clearInterval(checkPlayer);
                    // cue video dynamically once captions arrive
                }
            }, 100);
        }"""
    )

    next_video_button.click(
        fn=get_next_components,
        outputs=[caption_editor, current_video_id]
    )
    next_video_button.click(
        fn=lambda: False,
        outputs=editing_complete_checkbox
    )

    current_video_id.change(
        fn=None,
        inputs=current_video_id,
        outputs=None,
        js="""(videoId) => {
            if (window.ytPlayer && window.ytPlayer.cueVideoById) {
                console.log('[Video Load] cueVideoById', videoId);
                window.ytPlayer.cueVideoById(videoId);
            }
        }"""
    )

    caption_editor.select(
        fn=on_row_select,
        inputs=[caption_editor],
        outputs=[editing_panel, start_time_input, text_input, end_time_input, selected_row_idx, save_entry_button]
    )

    editing_complete_checkbox.input(
        fn=change_completion_status,
        inputs=editing_complete_checkbox
    )

    add_entry_button.click(
        fn=show_add_entry_form,
        outputs=[editing_panel, start_time_input, text_input, end_time_input, selected_row_idx, save_entry_button]
    )

    save_entry_button.click(
        fn=save_entry,
        inputs=[caption_editor, start_time_input, text_input, end_time_input,
                selected_row_idx, current_video_id],
        outputs=[caption_editor, editing_panel, save_result]
    )

    insert_start_time_button.click(
        fn=None, inputs=None, outputs=start_time_input,
        js="() => window.ytPlayer ? +window.ytPlayer.getCurrentTime().toFixed(3) : 0"
    )
    insert_end_time_button.click(
        fn=None, inputs=None, outputs=end_time_input,
        js="() => window.ytPlayer ? +window.ytPlayer.getCurrentTime().toFixed(3) : 0"
    )

    cancel_button.click(fn=cancel_edit, outputs=[editing_panel])

main_page.launch(share=True)