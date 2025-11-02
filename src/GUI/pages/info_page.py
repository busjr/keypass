import pyperclip
import webbrowser
import customtkinter as ctk
from utils.config_manager import load_settings
from setting import THEMES

class InfoPage(ctk.CTkFrame):
    def __init__(self, parent):

        # Загружаем настройки из JSON
        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]

        # Применяем цвета 
        self.widget_color = self.theme.get("windows", {}).get("info", {})

        # параметры из окна
        super().__init__(parent, corner_radius=15, fg_color=self.widget_color["bg"])

        # --- Заголовок ---
        ctk.CTkLabel(self, text="Информация о записи", font=("Arial", 18, "bold"), text_color=self.widget_color["title_text"]).pack(pady=10)

        # --- ИМЯ ---
        self.name_frame = ctk.CTkFrame(self, fg_color=self.widget_color["card_bg"], corner_radius=12)
        self.name_frame.pack(fill="x", padx=25, pady=(0, 12))

        self.name_label = ctk.CTkLabel(
            self.name_frame,
            text="Имя: ...",
            text_color=self.widget_color["title_text"],
            font=("Arial", 14),
            anchor="w"
        )
        self.name_label.pack(side="left", fill="x", expand=True, padx=20, pady=10)

        self.name_copy_btn = ctk.CTkButton(
            self.name_frame,
            text="Копировать",
            width=110,
            height=32,
            corner_radius=8,
            font=("Arial", 13),
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            command=lambda: self.copy("name")
        )
        self.name_copy_btn.pack(side="right", padx=15, pady=8)

        # --- ЛОГИН ---
        self.login_frame = ctk.CTkFrame(self, fg_color=self.widget_color["card_bg"], corner_radius=12)
        self.login_frame.pack(fill="x", padx=25, pady=(0, 12))

        self.login_label = ctk.CTkLabel(
            self.login_frame,
            text="Логин: ...",
            text_color=self.widget_color["title_text"],
            font=("Arial", 14),
            anchor="w"
        )
        self.login_label.pack(side="left", fill="x", expand=True, padx=20, pady=10)

        self.login_copy_btn = ctk.CTkButton(
            self.login_frame,
            text="Копировать",
            width=110,
            height=32,
            corner_radius=8,
            font=("Arial", 13),
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            command=lambda: self.copy("login")
        )
        self.login_copy_btn.pack(side="right", padx=15, pady=8)

        # --- ПАРОЛЬ ---
        self.pass_frame = ctk.CTkFrame(self, fg_color=self.widget_color["card_bg"], corner_radius=12)
        self.pass_frame.pack(fill="x", padx=25, pady=(0, 12))

        self.pass_label = ctk.CTkLabel(
            self.pass_frame,
            text="Пароль: ...",
            text_color=self.widget_color["title_text"],
            font=("Arial", 14),
            anchor="w"
        )
        self.pass_label.pack(side="left", fill="x", expand=True, padx=20, pady=10)

        self.pass_copy_btn = ctk.CTkButton(
            self.pass_frame,
            text="Копировать",
            width=110,
            height=32,
            corner_radius=8,
            font=("Arial", 13),
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            command=lambda: self.copy("password")
        )
        self.pass_copy_btn.pack(side="right", padx=15, pady=8)

        # --- ССЫЛКА ---
        self.link_frame = ctk.CTkFrame(self, fg_color=self.widget_color["card_bg"], corner_radius=12)
        self.link_frame.pack(fill="x", padx=25, pady=(0, 12))

        self.link_label = ctk.CTkLabel(
            self.link_frame,
            text="Сайт: ...",
            text_color=self.widget_color["title_text"],
            font=("Arial", 14),
            anchor="w"
        )
        self.link_label.pack(side="left", fill="x", expand=True, padx=20, pady=10)

        self.link_btn = ctk.CTkButton(
            self.link_frame,
            text="Открыть",
            width=110,
            height=32,
            corner_radius=8,
            font=("Arial", 13),
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            command=lambda: self.copy("url")
        )
        self.link_btn.pack(side="right", padx=15, pady=8)

        # Храним текущие данные
        self.current_data = {}

    def update_info(self, data: dict):
        """ Обновления данных """

        def cup(text, max_len=25):
            """Обрезает текст, если он длиннее max_len"""
            text = str(text or "—")
            return text if len(text) <= max_len else text[:max_len - 3] + "..."

        self.current_data = data or {}
        self.name_label.configure(text=f"Имя: {cup(data.get('name', '—'))}")
        self.login_label.configure(text=f"Логин: {cup(data.get('login', '—'))}")
        self.pass_label.configure(text=f"Пароль: {cup(data.get('password', '—'))}")
        self.link_label.configure(text=f"Сайт: {cup(data.get('url', '—'))}")

    def copy(self, field: str):
        """ Копирования данных """ # TODO упростить
        value = self.current_data.get(field, "")
        if not value:
            self.show_info("Поле пустое ⚠️")
            return

        if field == "url":
            if value.startswith("http"):
                webbrowser.open(value)
            else:
                self.show_info("Некорректная ссылка ⚠️")
            return

        pyperclip.copy(value)
        self.show_info("Текст скопирован ✅")

    def show_info(self, text):
        """ Вывод информационного окна """
        toast = ctk.CTkLabel(
            self,
            text=text,
            fg_color="#2a2c2c",
            text_color="#dcdcdc",
            font=("Arial", 13),
            corner_radius=8
        )
        toast.place(relx=0.5, rely=0.9, anchor="center")
        self.after(1500, toast.destroy)
