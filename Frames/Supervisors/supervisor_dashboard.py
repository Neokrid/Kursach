import tkinter as tk

class SupervisorDashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Личный кабинет супервайзера", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Список преподавателей", command=master.show_teacher_list).pack(pady=5)
        tk.Button(self, text="Выход", command=master.show_login).pack(pady=5)