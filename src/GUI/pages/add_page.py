import customtkinter as ctk
from utils.pass_generator import *
from utils.decrypt import decrypt
from utils.encrypt import encrypt
from utils.config_manager import load_settings
from setting import THEMES

class AddPage(ctk.CTkFrame):
    def __init__(self, parent, main_window):

        # Загружаем настройки из JSON
        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]

        # Применяем цвета 
        self.widget_color = self.theme.get("windows", {}).get("add", {})

        # параметры из окна
        super().__init__(parent, corner_radius=15, fg_color=self.widget_color["bg"])
        self.main_window = main_window
        self.parent = parent
        self.show_password = False

        ctk.CTkLabel(self, text="Добавить новую запись", font=("Arial", 18, "bold")).pack(pady=10)

        self.name_entry = ctk.CTkEntry(
            self, 
            placeholder_text="example.com",
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.name_entry.pack(fill="x", padx=10, pady=(4, 8))

        self.login_entry = ctk.CTkEntry(
            self, 
            placeholder_text="user@example.com",
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.login_entry.pack(fill="x", padx=10, pady=(4, 8))

        self.pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_frame.pack(fill="x", padx=10, pady=(4, 8))

        self.password_entry = ctk.CTkEntry(
            self.pass_frame,
            show="*",
            placeholder_text="Пароль: TSDIF77:W3E",
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10,
            border_width=1
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        pass_show_lbl = ctk.CTkLabel(
            self.pass_frame,
            text="👁", 
            text_color=self.widget_color["subtitle_text"], 
            height=15,
            width=50,
            cursor="hand2",
            fg_color=self.widget_color["entry_bg"],
            font=("Arial", 18, "bold")
        )
        pass_show_lbl.place(x=300, y=2)
        pass_show_lbl.bind("<Button-1>", lambda e: self.SH_password())

        self.generate_btn = ctk.CTkButton(
            self.pass_frame,
            text="🔄",
            font=("Arial", 18, "bold"),
            command=self.generate_pass,
            width=90,
            height=28,
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0
        )
        self.generate_btn.pack(side="right")

        self.url_entry = ctk.CTkEntry(
            self, 
            placeholder_text="https://example.com",
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"], 
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.url_entry.pack(fill="x", padx=10, pady=(4, 10))

        param_pass_frame = ctk.CTkFrame(self)
        param_pass_frame.pack(fill="x", padx=10, pady=(4, 8))

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

        # --- Вввод длины пароля ---
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

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=10, pady=(4, 8))

        save_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Сохранить", 
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0,
            command=self.save
        )
        save_btn.pack(fill="x")

    def SH_password(self):
        """ Скрытие/Открытие поле с паролем """
        if self.show_password:
            self.password_entry.configure(show="*")
        else:
            self.password_entry.configure(show="")
        self.show_password = not self.show_password

    def generate_pass(self):
        """ Генерация пароля """
        length = int(self.length_entry.get())
        en_latter = self.cb_en.get()
        ru_latter = self.cb_ru.get()
        lower = self.cb_lower.get()
        upper = self.cb_upper.get()
        special = self.cb_special.get()
        number = self.cb_number.get()
        password = generate_pass(length, en_latter, ru_latter, lower, upper, special, number)
        if password:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, password)

    def save(self):
        add_data = {
            "name": self.name_entry.get().strip(),
            "login": self.login_entry.get().strip(),
            "password": self.password_entry.get().strip(),
            "url": self.url_entry.get().strip(),
        }

        try:
            # читаем хранилище 
            data = decrypt(self.main_window.path, self.main_window.password)

            # Проверяем на дубликат в название
            for item in data["passwords"]:
                if item["name"].lower() == add_data["name"].lower():
                    print(f"{add_data['name']} уже существует") # TODO добавить уведомление
                    return

            # добавляем новую запись
            data["passwords"].append(add_data)

            # сохраняем обратно
            encrypt(self.main_window.path, self.main_window.password, data)

            # обновляем список на главном окне
            self.main_window.load_passwords(self.main_window.path, self.main_window.password)

            print("Запись успешно добавлена")
        except Exception as e:
            print("Ошибка при сохранении:", e)