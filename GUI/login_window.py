import os
import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image 
from GUI.create_storage_window import CreateStorageWindow
from GUI.main_window import MainWindow
from utils.decrypt import check_valid
from utils.config_manager import load_settings, save_settings
from setting import THEMES

class LoginWindow(ctk.CTk):
    """
    Первоначальное окно при запуске от него запускаются другие.
    """
    def __init__(self):
        super().__init__()

        # Загружаем настройки из JSON
        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]

        # Применяем цвета 
        ctk.set_appearance_mode(self.theme_name)
        self.configure(fg_color=self.theme["bg"])
        self.widget_color = self.theme.get("windows", {}).get("login", {})

        # Настройка окна
        self.title("Вход в хранилище")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 420) // 2
        self.geometry(f"500x420+{x}+{y}")

        ico_path = os.path.join(os.path.dirname(__file__), "image", "icon.ico")
        self.iconbitmap(ico_path)

        self.resizable(False, False)
        self.show_password = False
        
        # Обработчик закрытия окна
        # self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Иконка ---
        DIR = os.path.dirname(os.path.abspath(__file__))
        logo_img = ctk.CTkImage(light_image=Image.open(os.path.join(DIR, "image/1.png")), size=(80, 80))
        logo_label = ctk.CTkLabel(self, image=logo_img, text="")
        logo_label.pack()

        # --- Заголовок ---
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(10, 20))

        title_lbl1 = ctk.CTkLabel(title_frame, text="Вход в хранилище паролей", font=("Arial", 22, "bold"))
        title_lbl1.pack()

        title_lbl2 = ctk.CTkLabel(title_frame, text="Выберите зашифрованный файл с паролями и введите мастер-пароль", font=("Arial", 14), text_color="gray")
        title_lbl2.pack()

        # --- Зона с указыванием path ---
        path_label = ctk.CTkLabel(self, text="Файл с паролями:")
        path_label.pack(anchor="w", padx=20)

        path_frame = ctk.CTkFrame(self, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.path_edit = ctk.CTkEntry(
            path_frame, 
            placeholder_text="Путь\\до\\файла\\файл.aes", 
            height=40, 
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["subtitle_text"],
            fg_color=self.widget_color["entry_bg"],
            corner_radius=10, 
            border_width=1
        )
        self.path_edit.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            path_frame,
            text="Обзор",
            width=80,
            height=40, 
            text_color=self.widget_color["button_text"],
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0,
            command=self.select_file
        )
        browse_btn.pack(side="right")

        # --- Мастер пароль ---
        pass_lbl = ctk.CTkLabel(self, text="Мастер пароль:")
        pass_lbl.pack(anchor="w", padx=20)

        pass_frame = ctk.CTkFrame(self, fg_color="transparent" )
        pass_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.master_edit = ctk.CTkEntry(
            pass_frame,
            placeholder_text="Введите мастер-пароль",
            height=40, 
            width=510,
            show="*",
            placeholder_text_color=self.widget_color["entry_placeholder"], 
            text_color=self.widget_color["entry_text"],
            fg_color=self.widget_color["entry_bg"], 
            corner_radius=10, 
            border_width=1
        )
        self.master_edit.pack(side="left")

        pass_show_lbl = ctk.CTkLabel(
            pass_frame,
            text="👁", 
            text_color=self.widget_color["subtitle_text"], 
            height=30, 
            width=50,
            cursor="hand2",
            fg_color=self.widget_color["entry_bg"],
            font=("Arial", 22, "bold")
        )
        pass_show_lbl.place(x=400, y=4)
        pass_show_lbl.bind("<Button-1>", lambda e: self.SH_password())

        # --- Кнопка входа ---
        login_btn = ctk.CTkButton(
            self, 
            text="Войти",
            text_color=self.widget_color["button_text"],
            height=40,
            width=460,
            fg_color=self.widget_color["button_bg"],
            hover_color=self.widget_color["button_hover"],
            border_width=0,
            command=self.open_main_window
        )
        login_btn.pack(pady=(0, 15))

        # --- Кнопка создать\запомнить ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)

        self.chb_follow = ctk.CTkCheckBox(
            btn_frame, 
            text="Запомнить путь",
            border_width=1,
            hover_color=self.widget_color["checkbox_hover"],
            checkmark_color=self.widget_color["checkbox_checkmark"],
            fg_color=self.widget_color["checkbox_bg"],
            command=self.update_setting
            )
        self.chb_follow.pack(side="left")

        create_label = ctk.CTkLabel(btn_frame, text="Создать хранилище", text_color="#696969", cursor="hand2")
        create_label.pack(side="right")
        create_label.bind("<Button-1>", lambda e: CreateStorageWindow(self))

        # при старте проверям setting.json
        if self.settings.get("remember_path"):
            self.chb_follow.select()
            if self.settings.get("last_path"):
                self.path_edit.insert(0, self.settings["last_path"])
        else:
            self.chb_follow.deselect()

    def update_setting(self):
        """
        Сохраняем состояние чекбокса и путь. Тут мы сохраняет занчения и записываем в json (в Documents).
        Иначе стираем.
        """
        self.settings["remember_path"] = bool(self.chb_follow.get())

        if self.settings["remember_path"]:
            # если включено — сохраняем текущий путь, если есть
            current_path = self.path_edit.get().strip()
            if current_path:
                self.settings["last_path"] = current_path
        else:
            # если выключено — стираем путь
            self.settings["last_path"] = ""

        save_settings(self.settings)
        # print(self.settings) 


    def select_file(self):
        path_file = filedialog.askopenfilename(title="Выбрать файл")
        if path_file:
            self.path_edit.delete(0, "end")
            self.path_edit.insert(0, path_file)

    def SH_password(self):
        if self.show_password:
            self.master_edit.configure(show="*")
        else:
            self.master_edit.configure(show="")
        self.show_password = not self.show_password

    def open_main_window(self):
        path = self.path_edit.get()
        master = self.master_edit.get() # TODO удалять из памяти

        if check_valid(path, master):
            try:
                # self.destroy() # закрыть 
                self.withdraw() # скрыть 
                MainWindow(path, master)
            except Exception as e:
                print(f"Ошибка входа {e}") # TODO добавить окно или уведомление
                return
