import customtkinter as ctk
import tkinter as tk
import os
from utils.decrypt import decrypt
from utils.encrypt import encrypt
from utils.config_manager import load_settings, save_settings
from setting import THEMES

from GUI.pages.info_page import InfoPage
from GUI.pages.setting_page import SettingPage
from GUI.pages.edit_page import EditPage
from GUI.pages.add_page import AddPage

class MainWindow(ctk.CTkToplevel):
    def __init__(self, path, password):
        super().__init__()

        # Загружаем JSON
        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]

        # Применяем цвета 
        ctk.set_appearance_mode(self.theme_name)
        self.configure(fg_color=self.theme["bg"])
        self.widget_color = self.theme.get("windows", {}).get("main", {})

        # Настройка окна
        self.title("Менеджер паролей")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 450) // 2
        self.geometry(f"700x450+{x}+{y}")

        ico_path = os.path.join(os.path.dirname(__file__), "image", "icon.ico")
        self.after(250, lambda: self.iconbitmap(ico_path))

        self.protocol("WM_DELETE_WINDOW", self.on_close) # полное закрытие приложение

        # параметры из логина
        self.path = path
        self.password = password
        self.passwords = {}

        # --- ОСНОВНОЙ ФРЕЙМ ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both")

        # --- ЛЕВАЯ ПАНЕЛЬ ---
        self.left_frame = ctk.CTkFrame(main_frame, width=250, fg_color="transparent")
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Фрейм поиска
        search_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 5))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.search)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Поиск...",
            placeholder_text_color=self.widget_color["search_placeholder"],
            text_color=self.widget_color["search_text"],
            fg_color=self.widget_color["search_bg"],
            corner_radius=10,
            border_width=1
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.add_button = ctk.CTkButton(
            search_frame,
            text="+",
            width=40,
            text_color=self.widget_color["btn_text"],
            fg_color=self.widget_color["btn_bg"],
            hover_color=self.widget_color["btn_hover"],
            border_width=0,
            command=lambda: self.show_page("add")
        )
        self.add_button.pack(side="right")

        # Список паролей
        self.password_listbox = tk.Listbox(
            self.left_frame,
            height=20,
            bg=self.widget_color["list_bg"],           
            fg=self.widget_color["list_fg"],            
            selectbackground=self.widget_color["list_select_bg"],
            relief="flat",         
            borderwidth=10,          
            highlightthickness=0,    
        )
        self.password_listbox.pack(fill="both", expand=True, padx=0, pady=0, ipady=0, ipadx=0)
        self.password_listbox.bind("<<ListboxSelect>>", self.show_info)

        # --- ПРАВАЯ ПАНЕЛЬ ---
        self.right_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="transparent")
        self.right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Словарь страниц
        self.pages = {
            "info": InfoPage(self.right_frame),
            "settings": SettingPage(self.right_frame),
            "edit": EditPage(self.right_frame, self),
            "add": AddPage(self.right_frame, self)
        }

        self.show_page("info") # Показываем страницу по умолчанию

        # --- НИЖНИЕ КНОПКИ ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=5, pady=(5, 10))

        self.setting_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Настройки",
            fg_color=self.widget_color["btn_bg"], 
            text_color=self.widget_color["btn_text"],
            hover_color=self.widget_color["btn_hover"],
            command=lambda: self.show_page("settings")
        )
        self.setting_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.edit_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Изменить",
            fg_color=self.widget_color["btn_bg"], 
            text_color=self.widget_color["btn_text"],
            hover_color=self.widget_color["btn_hover"],
            command=self.edit_item
        )
        self.edit_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.delete_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Удалить",
            fg_color=self.widget_color["btn_bg"], 
            text_color=self.widget_color["btn_text"],
            hover_color=self.widget_color["btn_hover"],
            command=self.delete_item
        )
        self.delete_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.exit_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Выход",
            fg_color=self.widget_color["btn_bg"], 
            text_color=self.widget_color["btn_text"],
            hover_color=self.widget_color["btn_hover"],
            command=self.on_close # TODO может сделать возвращение в логин
        )
        self.exit_btn.pack(side="left", expand=True, fill="x", padx=5)

        # Загружаем пароли
        self.load_passwords(self.path, self.password)

        # Таймер
        self.timeout_seconds = self.settings.get("timeout")
        self.inactivity_timer = None
        self.reset_timer()

        # Отслеживание активности
        self.bind_all("<Any-KeyPress>", self.on_activity)
        self.bind_all("<Motion>", self.on_activity)

    def on_activity(self, event=None):
        """Срабатывает при любом движении / вводе"""
        self.reset_timer()

    def reset_timer(self):
        """Перезапуск таймера"""
        if self.inactivity_timer:
            self.after_cancel(self.inactivity_timer)

        ms = self.timeout_seconds * 60 * 1000
        self.inactivity_timer = self.after(int(ms), self.on_close)

    def search(self, *args):
        """Фильтрация списка по поисковому запросу"""
        query = self.search_var.get().lower()
        self.password_listbox.delete(0, "end")

        # если поиск пустой — показываем все записи
        if not query:
            for name in self.passwords.keys():
                self.password_listbox.insert("end", name)
            return

        # фильтруем по вхождению текста
        for name in self.passwords.keys():
            if query in name.lower():
                self.password_listbox.insert("end", name)


    def show_page(self, name: str):
        """Показать нужную страницу в правом фрейме"""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(expand=True, fill="both")


    def load_passwords(self, path, master):
        """Дешифровка и загрузка паролей"""
        try:
            data = decrypt(path, master)

            self.passwords = {item["name"]: item for item in data.get("passwords", [])}
            self.password_listbox.delete(0, "end")

            for name in self.passwords.keys():
                self.password_listbox.insert("end", name)

        except Exception as e:
            print("Ошибка загрузки паролей:", e)


    def show_info(self, event):
        """Показать данные выбранного пароля"""
        selection = self.password_listbox.curselection()
        if not selection:
            return
        key = self.password_listbox.get(selection[0])
        info = self.passwords.get(key, {})

        # Переключаемся на страницу info и обновляем данные
        self.show_page("info")
        self.pages["info"].update_info(info)


    def delete_item(self):
        """Удалить выбранный пароль"""
        selection = self.password_listbox.curselection()
        if not selection:
            return

        key = self.password_listbox.get(selection[0])
        data = decrypt(self.path, self.password)
        if not data:
            return

        items = data["passwords"]
        for item in items:
            if item.get("name") == key:
                items.remove(item) # Удаляем выбранную запись
                break

        encrypt(self.path, self.password, data)
        self.load_passwords(self.path, self.password)


    def edit_item(self):
        """Изменить выбранный пароль"""
        selection = self.password_listbox.curselection()
        if not selection:
            return

        key = self.password_listbox.get(selection[0])
        data = decrypt(self.path, self.password)
        if not data:
            return

        items = data["passwords"]
        for item in items:
            if item.get("name") == key:
                self.show_page("edit")
                self.pages["edit"].update_info(item)

    def on_close(self):
        """Корректное закрытие приложения"""
        self.destroy() # TODO сделать выход в логин или лучше оставить
        self.quit()
