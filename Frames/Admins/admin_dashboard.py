import tkinter as tk

class AdminDashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Личный кабинет администратора", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Пользователи", command=master.show_user_list).pack(pady=5)
        tk.Button(self, text="Выход", command=master.show_login).pack(pady=5)