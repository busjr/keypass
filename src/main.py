from GUI.login_window import LoginWindow
import customtkinter as ctk

if __name__ == "__main__":
    # Запуск окна с логином
    ctk.set_appearance_mode("System")
    app = LoginWindow()
    app.mainloop()
