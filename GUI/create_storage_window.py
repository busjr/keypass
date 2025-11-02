import customtkinter as ctk
import os
import pyperclip
from customtkinter import filedialog
from setting import *
from utils.pass_generator import *
from utils.encrypt import *
from utils.config_manager import load_settings, save_settings
from setting import THEMES

class CreateStorageWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # Загружаем настройки из JSON
        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]

        # Применяем цвета 
        ctk.set_appearance_mode(self.theme_name)
        self.configure(fg_color=self.theme["bg"])
        self.widget_color = self.theme.get("windows", {}).get("create_storage", {})

        # Настройка окна
        self.title("Создать хранилище")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 500) // 2
        y = (screen_height - 420) // 2

        self.geometry(f"500x420+{x}+{y}")
        self.resizable(False, False)

        ico_path = os.path.join(os.path.dirname(__file__), "image", "icon.ico")
        self.after(250, lambda: self.iconbitmap(ico_path))

        self.show_password = False

        # Модальное окно
        self.transient(master)
        self.grab_set()
        self.focus()

        # Скрываем основное окно входа
        # if master and hasattr(master, 'withdraw'):
        master.withdraw()

        path_lbl = ctk.CTkLabel(self, text="Путь для хранилища:")
        path_lbl.pack(anchor="w", padx=20, pady=(15, 0))

        path_frame = ctk.CTkFrame(self, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.path_entry = ctk.CTkEntry(
            path_frame, 
            placeholder_text="Укажите путь для хранилища (.aes)",
            height=40,
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            path_frame, 
            text="Обзор", 
            width=90, 
            height=40,
            command=self.save_file,
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0
        )
        browse_btn.pack(side="right")

        pass_lbl = ctk.CTkLabel(self, text="Мастер-пароль:")
        pass_lbl.pack(anchor="w", padx=20)

        first_pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        first_pass_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.first_master_entry = ctk.CTkEntry(
            first_pass_frame, 
            placeholder_text="Введите мастер-пароль", 
            show="*",
            height=40,
            placeholder_text_color=self.widget_color["entry_placeholder"],
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.first_master_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        pass_show_lbl = ctk.CTkLabel(
            first_pass_frame,
            text="👁", 
            text_color=self.widget_color["subtitle_text"], 
            height=30, 
            width=50,
            cursor="hand2",
            fg_color=self.widget_color["entry_bg"],
            font=("Arial", 22, "bold")
        )
        pass_show_lbl.place(x=305, y=3)
        pass_show_lbl.bind("<Button-1>", lambda e: self.SH_password())

        copy_btn = ctk.CTkButton(
            first_pass_frame, 
            text="📋", 
            font=("Arial", 22, "bold"),
            width=90, 
            height=40,
            command=self.copy,
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0
        )
        copy_btn.pack(side="right")

        last_pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        last_pass_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.last_master_entry = ctk.CTkEntry(
            last_pass_frame, 
            placeholder_text="Повторите мастер-пароль", 
            show="*",
            height=40,
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.last_master_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        generate_btn = ctk.CTkButton(
            last_pass_frame, 
            text="🔄", 
            font=("Arial", 22, "bold"),
            command=self.generate_pass,
            width=90, 
            height=40,
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0
        )
        generate_btn.pack(side="right")

        param_pass_frame = ctk.CTkFrame(self, width=90, height=40)
        param_pass_frame.pack(fill="x", padx=20, pady=(0, 15))

        title_param = ctk.CTkLabel(param_pass_frame, text="Параметры для генерации пароля:")
        title_param.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 10), sticky="w")

        # Настраиваем сетку — 3 равные колонки
        param_pass_frame.grid_columnconfigure(0, weight=1)
        param_pass_frame.grid_columnconfigure(1, weight=1)
        param_pass_frame.grid_columnconfigure(2, weight=1)
        param_pass_frame.grid_columnconfigure(3, weight=1)

        # Хранение значения checkbox
        var_cb_en = ctk.IntVar(value=1)
        var_cb_ru = ctk.IntVar(value=0)
        var_cb_upper = ctk.IntVar(value=1)
        var_cb_number = ctk.IntVar(value=1)
        var_cb_special = ctk.IntVar(value=1)
        var_cb_lower = ctk.IntVar(value=1)

        # --- Ряд 1 ---
        self.cb_en = ctk.CTkCheckBox(
            param_pass_frame, 
            variable=var_cb_en,
            text="ABCD...",
            border_width=1, 
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"], 
            fg_color=self.widget_color["checkbox_bg"]
        )
        self.cb_en.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.cb_ru = ctk.CTkCheckBox(
            param_pass_frame, 
            variable=var_cb_ru,
            text="АБВГ...",
            border_width=1, 
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"], 
            fg_color=self.widget_color["checkbox_bg"]
        )
        self.cb_ru.grid(row=1, column=1, padx=5, pady=5, sticky="")

        self.cb_upper = ctk.CTkCheckBox(
            param_pass_frame, 
            variable=var_cb_upper,
            text="Верхний регистр",
            border_width=1, 
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"], 
            fg_color=self.widget_color["checkbox_bg"]
        )
        self.cb_upper.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # --- Ряд 2 ---
        self.cb_number = ctk.CTkCheckBox(
            param_pass_frame,
            variable=var_cb_number,
            text="1234...",
            border_width=1, 
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"], 
            fg_color=self.widget_color["checkbox_bg"]
        )
        self.cb_number.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.cb_special = ctk.CTkCheckBox(
            param_pass_frame, 
            variable=var_cb_special,
            text="!@#$...",
            border_width=1, 
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"], 
            fg_color=self.widget_color["checkbox_bg"]
        )
        self.cb_special.grid(row=2, column=1, padx=5, pady=5, sticky="")

        self.cb_lower = ctk.CTkCheckBox(
            param_pass_frame,
            variable=var_cb_lower,
            text="Нижний регистр",
            border_width=1,
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"], 
            fg_color=self.widget_color["checkbox_bg"]
        )
        self.cb_lower.grid(row=2, column=2, padx=5, pady=5, sticky="e")

        # --- Input ---
        self.length_entry = ctk.CTkEntry(
            param_pass_frame,
            placeholder_text="Длина\nпароля:",
            height=50,
            width=50,
            placeholder_text_color=self.widget_color["entry_placeholder"],
            text_color=self.widget_color["entry_text"],
            fg_color=self.widget_color["entry_bg"],
            corner_radius=10,
            border_width=1,
            justify="center"
        )
        self.length_entry.insert(0, "12")
        self.length_entry.grid(row=1, column=3, rowspan=2, padx=10, pady=5, sticky="nsew")

        # Чтобы поле растягивалось при изменении окна
        # param_pass_frame.grid_rowconfigure(3, weight=1)

        # Фрейм для кнопок создания и возврата (в ряд)
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Кнопка "Назад"
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="Назад", 
            height=40,
            command=self.go_back,
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0
        )
        back_btn.pack(side="right", fill="x", expand=True)

        # Кнопка "Создать"
        create_btn = ctk.CTkButton(
            buttons_frame, 
            text="Создать", 
            height=40,
            command=self.create_storage,
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0
        )
        create_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.protocol("WM_DELETE_WINDOW", self.go_back) # проверка на закрытие окна


    def copy(self):
        value = self.first_master_entry.get()
        pyperclip.copy(value)
    
    def SH_password(self):
        if self.show_password:
            self.first_master_entry.configure(show="*")
            self.last_master_entry.configure(show="*")
        else:
            self.first_master_entry.configure(show="")
            self.last_master_entry.configure(show="")
        self.show_password = not self.show_password

    def generate_pass(self):
        length = int(self.length_entry.get())
        en_latter = self.cb_en.get()
        ru_latter = self.cb_ru.get()
        lower = self.cb_lower.get()
        upper = self.cb_upper.get()
        special = self.cb_special.get()
        number = self.cb_number.get()
        master = generate_pass(length, en_latter, ru_latter, lower, upper, special, number)
        if master:
            self.first_master_entry.delete(0, "end")
            self.first_master_entry.insert(0, master)

            self.last_master_entry.delete(0, "end")
            self.last_master_entry.insert(0, master)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".aes",
            filetypes=[("AES vault", "*.aes"), ("All files", "*.*")],
            title="Сохранить хранилище как..."
        )
        if file_path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, file_path)

    def create_storage(self):
        path_file = self.path_entry.get().strip()
        first_master_entry = self.first_master_entry.get()
        last_master_entry = self.last_master_entry.get()
        if not path_file or not (first_master_entry or last_master_entry):
            print("CreateStorageWindow: путь или пароль не указан")
            return
        
        if first_master_entry == last_master_entry:
            encrypt(path_file, first_master_entry)
            self.destroy()
            self.master.deiconify()

    def go_back(self):
        """Возврат к окну входа"""
        self.destroy()
        self.master.deiconify()