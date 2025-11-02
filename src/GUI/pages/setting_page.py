import customtkinter as ctk
from utils.config_manager import load_settings, save_settings
from setting import THEMES
import sys
import os

class SettingPage(ctk.CTkFrame):
    def __init__(self, parent):

        # Загружаем настройки из JSON
        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]

        # Применяем цвета 
        self.widget_color = self.theme.get("windows", {}).get("settings", {})

        # параметры окна
        super().__init__(parent, corner_radius=15, fg_color=self.widget_color["bg"])

        # --- Заголовок ---
        title = ctk.CTkLabel(self, text="Настройки", font=("Arial", 18, "bold"), text_color=self.widget_color["title_text"])
        title.pack(pady=(20, 10))

        # --- Выбор темы ---
        theme_frame = ctk.CTkFrame(self, fg_color=self.widget_color["panel_bg"], corner_radius=10)
        theme_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(theme_frame, text="Тема приложения:", text_color=self.widget_color["title_text"]).pack(side="left", padx=10, pady=10)

        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode().lower())
        theme_selector = ctk.CTkOptionMenu(
            theme_frame, 
            values=["light", "dark"],
            variable=self.theme_var,
            dropdown_fg_color=self.widget_color["entry_bg"],
            button_color=self.widget_color["button_bg"],
            fg_color=self.widget_color["button_bg"],
            button_hover_color=self.widget_color["button_hover"],
            text_color=self.widget_color["text_color"],
            # command=self.change_theme
        )
        theme_selector.pack(side="right", padx=10, pady=10)

        # --- Настройка авто-выхода ---
        timeout_frame = ctk.CTkFrame(self, fg_color=self.widget_color["panel_bg"], corner_radius=10)
        timeout_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(timeout_frame, text="Авто-выход через (минут):", text_color=self.widget_color["title_text"]).pack(side="left", padx=10, pady=10)

        self.timeout_var = ctk.StringVar(value="15")
        timeout_entry = ctk.CTkEntry(
            timeout_frame, 
            textvariable=self.timeout_var,
            width=60, 
            justify="center", 
            fg_color=self.widget_color["entry_bg"],
            border_width=1, 
            corner_radius=8
        )
        timeout_entry.pack(side="right", padx=10, pady=10)

        # --- Настройка авто-запуска ---
        # autostart = ctk.CTkFrame(self, fg_color=self.widget_color["panel_bg"], corner_radius=10)
        # autostart.pack(padx=20, pady=10, fill="x")

        # ctk.CTkLabel(autostart, text="Авто-запуск при запуске OC:", text_color=self.widget_color["title_text"]).pack(side="left", padx=10, pady=10)

        # cb_autostart = ctk.CTkCheckBox(
        #     autostart,
        #     text="",
        #     corner_radius=5,
        #     width=20,
        #     height=20,
        #     border_width=1,
        #     hover_color=self.widget_color["button_hover"],
        #     checkmark_color=self.widget_color["entry_bg"],
        #     fg_color=self.widget_color["button_hover"]
        # )
        # cb_autostart.pack(side="right", padx=10, pady=10)

        # --- Кнопка сохранить ---
        save_button = ctk.CTkButton(
            self, 
            text="Сохранить настройки",
            width=20,
            height=40,
            fg_color=self.widget_color["button_bg"], 
            hover_color=self.widget_color["button_hover"],
            text_color=self.widget_color["button_text"],
            command=self.save_settings
        )
        save_button.pack(padx=20, pady=10, fill="x")

    def change_theme(self, mode):
        """Изменение темы и сохраняем в json"""
        ctk.set_appearance_mode(mode)
        self.settings["theme"] = mode
        save_settings(self.settings)

    def change_timeout(self, time):
        """Изменение timeout и сохраняем в json"""
        self.settings["timeout"] = int(time)
        save_settings(self.settings)

    def on_close(self):
        """Корректное закрытие приложения"""
        self.destroy()
        self.quit()

    def restart_app(self):
        self.destroy()
        app = sys.executable
        os.execl(app, app, *sys.argv)

    def save_settings(self):
        """Приминяем настройки"""
        theme = self.theme_var.get()
        timeout = self.timeout_var.get()
        # autostart = self.cb_autostart.get()

        self.change_theme(theme)
        self.change_timeout(timeout)
        self.restart_app()
