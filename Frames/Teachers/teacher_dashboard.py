import tkinter as tk


class TeacherDashboard(tk.Frame):
    def __init__(self, master, teacher_id):
        super().__init__(master)
        self.master = master
        self.teacher_id = teacher_id
        tk.Label(self, text="Личный кабинет преподавателя", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Список Дисциплин", command=self.show_my_subjects).pack(pady=5)
        tk.Button(self, text="Выход", command=master.show_login).pack(pady=5)
    
    def show_my_subjects(self):
        self.master.show_my_subjects_frame(self.teacher_id)