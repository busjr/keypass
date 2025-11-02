BUFFER_SIZE = 64 * 1024
APP_NAME = "keypass"
APP_VERSION = "1.0.0"

THEMES = {
    "dark": {
        "bg": "#262626",
        "fg": "#2a2a2a",
        "text_color": "#dcdcdc",

        "windows": {

            "login": {
                "bg": "#1f1f1f",
                "title_text": "#dcdcdc",
                "subtitle_text": "#696969",
                "entry_placeholder": "#696969",
                "entry_text": "#dcdcdc",
                "entry_bg": "#262626",
                "button_text": "#cfcfcf",
                "button_bg": "#2a2a2a",
                "button_hover": "#333333",
                "checkbox_checkmark": "#1f1f1f",
                "checkbox_bg": "#2a2c2c",
                "checkbox_hover": "#343434",
                "panel_bg": "#1f1f1f",
                "card_bg": "#262626"
            },

            "main": {
                "bg": "#1f1f1f",
                "list_bg": "#1f1f1f",
                "list_fg": "#dcdcdc",
                "list_select_bg": "#2a2c2c",
                "search_placeholder": "#696969",
                "search_text": "#dcdcdc",
                "search_bg": "#262626",
                "btn_text": "#cfcfcf",
                "btn_bg": "#1f1f1f",
                "btn_hover": "#333333",
                "panel_bg": "#1f1f1f",
                "card_bg": "#262626"
            },

            "create_storage": {
                "bg": "#1f1f1f",
                "title_text": "#dcdcdc",
                "subtitle_text": "#696969",
                "entry_placeholder": "#696969",
                "entry_text": "#dcdcdc",
                "entry_bg": "#262626",
                "button_text": "#cfcfcf",
                "button_bg": "#2a2a2a",
                "button_hover": "#333333",
                "checkbox_checkmark": "#1f1f1f",
                "checkbox_bg": "#2a2c2c",
                "checkbox_hover": "#343434",
                "panel_bg": "#2a2a2a",
                "card_bg": "#262626"
            },

            "add": {
                "bg": "#1f1f1f",
                "subtitle_text": "#696969",
                "entry_placeholder": "#696969",
                "entry_text": "#dcdcdc",
                "entry_bg": "#262626",
                "button_text": "#cfcfcf",
                "button_bg": "#2a2a2a",
                "button_hover": "#333333",
                "checkbox_checkmark": "#1f1f1f",
                "checkbox_bg": "#2a2c2c",
                "checkbox_hover": "#343434",
                "panel_bg": "#1f1f1f",
                "card_bg": "#262626"
            },

            "edit": {
                "bg": "#1f1f1f",
                "subtitle_text": "#696969",
                "entry_placeholder": "#696969",
                "entry_text": "#dcdcdc",
                "entry_bg": "#262626",
                "button_text": "#cfcfcf",
                "button_bg": "#2a2a2a",
                "button_hover": "#333333",
                "checkbox_checkmark": "#1f1f1f",
                "checkbox_bg": "#2a2c2c",
                "checkbox_hover": "#343434",
                "panel_bg": "#1f1f1f",
                "card_bg": "#262626"
            },

            "info": {
                "bg": "#1f1f1f",
                "title_text": "#dcdcdc",
                "button_text": "#cfcfcf",
                "button_bg": "#2a2a2a",
                "button_hover": "#333333",
                "panel_bg": "#1f1f1f",
                "card_bg": "#262626"
            },

            "settings": {
                "bg": "#1f1f1f",
                "title_text": "#dcdcdc",
                "text_color": "#dcdcdc",
                "button_text": "#cfcfcf",
                "button_bg": "#2a2a2a",
                "button_hover": "#333333",
                "entry_bg": "#262626",
                "panel_bg": "#2a2a2a",
                "card_bg": "#262626"
            }
        }
    },

    "light": {
        "bg": "#efefef",
        "fg": "#e5e5e5",
        "text_color": "#1f1f1f",

        "windows": {

            "login": {
                "bg": "#efefef",
                "title_text": "#1f1f1f",
                "subtitle_text": "#5a5a5a",
                "entry_placeholder": "#7d7d7d",
                "entry_text": "#1f1f1f",
                "entry_bg": "#e0e0e0",
                "button_text": "#1f1f1f",
                "button_bg": "#dadada",
                "button_hover": "#cfcfcf",
                "checkbox_checkmark": "#efefef",
                "checkbox_bg": "#d2d2d2",
                "checkbox_hover": "#c5c5c5",
                "panel_bg": "#f4f4f4",
                "card_bg": "#e6e6e6"
            },

            "main": {
                "bg": "#efefef",
                "list_bg": "#e0e0e0",
                "list_fg": "#1f1f1f",
                "list_select_bg": "#d6d6d6",
                "search_placeholder": "#7d7d7d",
                "search_text": "#1f1f1f",
                "search_bg": "#dedede",
                "btn_text": "#1f1f1f",
                "btn_bg": "#dadada",
                "btn_hover": "#cfcfcf",
                "panel_bg": "#f4f4f4",
                "card_bg": "#e6e6e6"
            },

            "create_storage": {
                "bg": "#e0e0e0",
                "title_text": "#1f1f1f",
                "subtitle_text": "#5a5a5a",
                "entry_placeholder": "#7d7d7d",
                "entry_text": "#1f1f1f",
                "entry_bg": "#e0e0e0",
                "button_text": "#1f1f1f",
                "button_bg": "#dadada",
                "button_hover": "#cfcfcf",
                "checkbox_checkmark": "#efefef",
                "checkbox_bg": "#d2d2d2",
                "checkbox_hover": "#c5c5c5",
                "panel_bg": "#e6e6e6",
                "card_bg": "#dedede"
            },

            "add": {
                "bg": "#e0e0e0",
                "subtitle_text": "#5a5a5a",
                "entry_placeholder": "#7d7d7d",
                "entry_text": "#1f1f1f",
                "entry_bg": "#e0e0e0",
                "button_text": "#1f1f1f",
                "button_bg": "#dadada",
                "button_hover": "#cfcfcf",
                "checkbox_checkmark": "#efefef",
                "checkbox_bg": "#d2d2d2",
                "checkbox_hover": "#c5c5c5",
                "panel_bg": "#f4f4f4",
                "card_bg": "#e6e6e6"
            },

            "edit": {
                "bg": "#e0e0e0",
                "subtitle_text": "#5a5a5a",
                "entry_placeholder": "#7d7d7d",
                "entry_text": "#1f1f1f",
                "entry_bg": "#e0e0e0",
                "button_text": "#1f1f1f",
                "button_bg": "#dadada",
                "button_hover": "#cfcfcf",
                "checkbox_checkmark": "#efefef",
                "checkbox_bg": "#d2d2d2",
                "checkbox_hover": "#c5c5c5",
                "panel_bg": "#f4f4f4",
                "card_bg": "#e6e6e6"
            },

            "info": {
                "bg": "#e0e0e0",
                "title_text": "#1f1f1f",
                "button_text": "#1f1f1f",
                "button_bg": "#dadada",
                "button_hover": "#cfcfcf",
                "panel_bg": "#f4f4f4",
                "card_bg": "#e6e6e6"
            },

            "settings": {
                "bg": "#dedede",
                "title_text": "#1f1f1f",
                "text_color": "#1f1f1f",
                "button_text": "#1f1f1f",
                "button_bg": "#dadada",
                "button_hover": "#cfcfcf",
                "entry_bg": "#e0e0e0",
                "panel_bg": "#e6e6e6",
                "card_bg": "#dedede"
            }
        }
    }
}


DEFAULT_SETTINGS = {
    "theme": "dark",
    "timeout": 15,
    "autostart": False,
    "remember_path": False,
    "last_path": ""
}
