# Localization strings for the Caption Editor app

# Set the active language here: "en" or "uk"
LANGUAGE = "uk"

STRINGS = {
    "en": {
        # Header and login
        "app_title": "Caption Editor",
        "please_log_in": "Please log in via Hugging Face",
        "logged_in_as": "Logged in as",
        "log_in_button": "Log in",
        
        # Main interface
        "next_button": "Finish this video and go to next",
        "add_entry_button": "Add Entry",
        
        # Table headers
        "header_start": "Start",
        "header_text": "Text",
        "header_end": "End",
        
        # Edit form
        "edit_caption_title": "Edit Caption Entry",
        "start_time_label": "Start Time (seconds)",
        "caption_text_label": "Caption Text",
        "caption_text_placeholder": "Enter caption text...",
        "end_time_label": "End Time (seconds)",
        "insert_current_time": "Insert Video Current Time",
        "save_entry_button": "Save Entry",
        "update_entry_button": "Update Entry",
        "add_entry_button_form": "Add Entry",
        "cancel_button": "Cancel",
        
        # Messages
        "please_sign_in": "Please sign in to save changes",
        "start_less_than_end": "Start time must be less than end time",
        "text_cannot_be_empty": "Text cannot be empty",
        "save_successful": "Save successful!",
        "save_failed": "Save failed:",
        "invalid_time_format": "Invalid time format:",
        "error": "Error:",
    },
    "uk": {
        # Header and login
        "app_title": "Редактор субтитрів",
        "please_log_in": "Будь ласка, увійдіть через Hugging Face",
        "logged_in_as": "Ви увійшли як",
        "log_in_button": "Увійти",
        
        # Main interface
        "next_button": "Завершити відео і перейти до наступного",
        "add_entry_button": "Додати субтитр",
        
        # Table headers
        "header_start": "Початок",
        "header_text": "Текст",
        "header_end": "Кінець",
        
        # Edit form
        "edit_caption_title": "Редагувати субтитр",
        "start_time_label": "Час початку (секунди)",
        "caption_text_label": "Текст субтитру",
        "caption_text_placeholder": "Введіть текст субтитру...",
        "end_time_label": "Час кінця (секунди)",
        "insert_current_time": "Вставити поточний час відео",
        "save_entry_button": "Зберегти запис",
        "update_entry_button": "Оновити запис",
        "add_entry_button_form": "Додати запис",
        "cancel_button": "Скасувати",
        
        # Messages
        "please_sign_in": "Будь ласка, увійдіть, щоб зберегти зміни",
        "start_less_than_end": "Час початку повинен бути менше часу кінця",
        "text_cannot_be_empty": "Текст не може бути порожнім",
        "save_successful": "Успішно збережено!",
        "save_failed": "Помилка збереження:",
        "invalid_time_format": "Невірний формат часу:",
        "error": "Помилка:",
    }
}

def get_string(key):
    """Get localized string by key"""
    return STRINGS[LANGUAGE].get(key, key)
