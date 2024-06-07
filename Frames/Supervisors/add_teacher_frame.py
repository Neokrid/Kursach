import tkinter as tk
from tkinter import messagebox
import csv

class AddTeacherFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Добавить преподавателя", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self, text="Логин:").pack(pady=5)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack(pady=5)

        tk.Label(self, text="Пароль:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self, text="ФИО:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Должность:").pack(pady=5)
        self.position_entry = tk.Entry(self)
        self.position_entry.pack(pady=5)

        tk.Label(self, text="Стаж работы:").pack(pady=5)
        self.experience_entry = tk.Entry(self)
        self.experience_entry.pack(pady=5)

        tk.Label(self, text="Ученая степень:").pack(pady=5)
        self.degree_entry = tk.Entry(self)
        self.degree_entry.pack(pady=5)

        tk.Label(self, text="Специальность:").pack(pady=5)
        self.specialty_entry = tk.Entry(self)
        self.specialty_entry.pack(pady=5)

        tk.Button(self, text="Подтвердить", command=self.add_teacher).pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Button(self, text="Назад", command=self.master.show_teacher_list).pack(side=tk.LEFT, padx=10, pady=10)

    def add_teacher(self):
        # Get the input data and add it to the teacher list
        login = self.login_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        position = self.position_entry.get()
        experience = self.experience_entry.get()
        degree = self.degree_entry.get()
        specialty = self.specialty_entry.get()

        teacher_id = self.generate_teacher_id()

        try:
            with open("Teachers.csv", "a", newline='', encoding='utf-8') as teachers_file:
                writer = csv.writer(teachers_file)
                writer.writerow([teacher_id, name, degree, position, experience, specialty])

            with open("Accounts.csv", "a", newline='', encoding='utf-8') as accounts_file:
                writer = csv.writer(accounts_file)
                writer.writerow([teacher_id, login, password])

            messagebox.showinfo("Успех", "Преподаватель успешно добавлен.")
            self.master.show_teacher_list()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def generate_teacher_id(self):
        try:
            with open("Teachers.csv", newline='', encoding='utf-8') as teachers_file:
                teachers = list(csv.reader(teachers_file))
                if teachers:
                    last_id = int(teachers[-1][0])
                    return str(last_id + 1)
                else:
                    return "301"  # First teacher ID
        except FileNotFoundError:
            return "301"  # First teacher ID
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при генерации ID: {e}")
            return None