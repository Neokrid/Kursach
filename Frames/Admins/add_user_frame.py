import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class AddUserFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.login_entry = None
        self.password_entry = None
        self.degree_entry = None
        self.position_entry = None
        self.experience_entry = None
        self.specialty_entry = None
        self.group_entry = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Добавить пользователя", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self, text="Тип аккаунта:").pack(pady=5)
        self.role_var = tk.StringVar()
        roles = ["Администратор", "Супервайзер", "Преподаватель", "Студент"]
        self.role_combobox = ttk.Combobox(self, textvariable=self.role_var, values=roles)
        self.role_combobox.pack(pady=5)
        self.role_combobox.bind("<<ComboboxSelected>>", self.update_form_fields)

        self.fields_frame = tk.Frame(self)
        self.fields_frame.pack(pady=10)

        self.update_form_fields()

        tk.Button(self, text="Назад", command=self.master.show_user_list).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Подтвердить", command=self.add_user).pack(side=tk.RIGHT, padx=10, pady=10)

    def update_form_fields(self, event=None):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        role = self.role_var.get()

        tk.Label(self.fields_frame, text="ФИО:").pack(pady=5)
        self.name_entry = tk.Entry(self.fields_frame)
        self.name_entry.pack(pady=5)

        if role != "Студент":
            tk.Label(self.fields_frame, text="Логин:").pack(pady=5)
            self.login_entry = tk.Entry(self.fields_frame)
            self.login_entry.pack(pady=5)

            tk.Label(self.fields_frame, text="Пароль:").pack(pady=5)
            self.password_entry = tk.Entry(self.fields_frame, show="*")
            self.password_entry.pack(pady=5)

        if role == "Преподаватель":
            tk.Label(self.fields_frame, text="Ученая степень:").pack(pady=5)
            self.degree_entry = tk.Entry(self.fields_frame)
            self.degree_entry.pack(pady=5)

            tk.Label(self.fields_frame, text="Должность:").pack(pady=5)
            self.position_entry = tk.Entry(self.fields_frame)
            self.position_entry.pack(pady=5)

            tk.Label(self.fields_frame, text="Опыт работы:").pack(pady=5)
            self.experience_entry = tk.Entry(self.fields_frame)
            self.experience_entry.pack(pady=5)

            tk.Label(self.fields_frame, text="Специальность:").pack(pady=5)
            self.specialty_entry = tk.Entry(self.fields_frame)
            self.specialty_entry.pack(pady=5)

        if role == "Студент":
            tk.Label(self.fields_frame, text="Группа:").pack(pady=5)
            self.group_entry = tk.Entry(self.fields_frame)
            self.group_entry.pack(pady=5)

    def add_user(self):
        name = self.name_entry.get()
        role = self.role_var.get()

        # Проверка существования виджетов и их значения
        login = self.login_entry.get() if self.login_entry and self.login_entry.winfo_exists() else ''
        password = self.password_entry.get() if self.password_entry and self.password_entry.winfo_exists() else ''
        degree = self.degree_entry.get() if self.degree_entry and self.degree_entry.winfo_exists() else ''
        position = self.position_entry.get() if self.position_entry and self.position_entry.winfo_exists() else ''
        experience = self.experience_entry.get() if self.experience_entry and self.experience_entry.winfo_exists() else ''
        specialty = self.specialty_entry.get() if self.specialty_entry and self.specialty_entry.winfo_exists() else ''
        group = self.group_entry.get() if self.group_entry and self.group_entry.winfo_exists() else ''

        if role != "Студент" and (not login or not password):
            messagebox.showerror("Error", "Логин и пароль обязательны для не-студентов")
            return

        user_id = self.generate_new_id(role)
        self.add_user_to_files(user_id, name, login, password, degree, position, experience, specialty, group, role)

        self.master.show_user_list()

    def generate_new_id(self, role):
        prefix = ''
        role_file = ''

        if role == "Администратор":
            prefix = '1'
            role_file = "Admins.csv"
        elif role == "Супервайзер":
            prefix = '2'
            role_file = "Supervisors.csv"
        elif role == "Преподаватель":
            prefix = '3'
            role_file = "Teachers.csv"
        elif role == "Студент":
            prefix = '4'
            role_file = "Students.csv"

        max_id = 0

        try:
            with open(role_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    current_id = int(row['ID_Accounts'])
                    if current_id // 100 == int(prefix):  # Ensure the current ID belongs to the current role
                        max_id = max(max_id, current_id)

        except FileNotFoundError:
            pass

        new_id = max_id + 1 if max_id != 0 else int(prefix + '01')
        return str(new_id)

    def add_user_to_files(self, user_id, name, login, password, degree, position, experience, specialty, group, role):
        try:
            if role != "Студент":
                with open("Accounts.csv", 'a', newline='', encoding='utf-8') as accounts_file:
                    account_writer = csv.writer(accounts_file)
                    account_writer.writerow([user_id, login, password])

            role_file = ''
            role_fields = []
            role_data = []

            if role == "Администратор":
                role_file = "Admins.csv"
                role_fields = ['ID_Accounts', 'Name']
                role_data = [user_id, name]

            elif role == "Супервайзер":
                role_file = "Supervisors.csv"
                role_fields = ['ID_Accounts', 'Name']
                role_data = [user_id, name]

            elif role == "Преподаватель":
                role_file = "Teachers.csv"
                role_fields = ['ID_Accounts', 'Name', 'Degree', 'Position', 'Experience', 'Specialty']
                role_data = [user_id, name, degree, position, experience, specialty]

            elif role == "Студент":
                role_file = "Students.csv"
                role_fields = ['ID_Accounts', 'Name', 'Group']
                role_data = [user_id, name, group]

            with open(role_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(role_data)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the user: {e}")