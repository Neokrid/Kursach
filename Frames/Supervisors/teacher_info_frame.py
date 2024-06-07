import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class TeacherInfoFrame(tk.Frame):
    def __init__(self, master, teacher):
        super().__init__(master)
        self.master = master
        self.teacher = teacher
        self.create_widgets()
        self.load_teacher_info()

    def create_widgets(self):
        tk.Label(self, text="Информация о преподавателе", font=("Helvetica", 16)).pack(pady=10)

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

        tk.Button(self, text="Редактировать", command=self.edit_teacher).pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Button(self, text="Редактировать расписание", command=self.edit_schedule).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Назад", command=self.master.show_teacher_list).pack(side=tk.LEFT, padx=10, pady=10)

    def load_teacher_info(self):
        teacher_id = str(self.teacher[2])
        account_info = None
        teacher_info = None

        # Load account info
        try:
            with open("Accounts.csv", newline='', encoding='utf-8') as accounts_file:
                account_reader = csv.DictReader(accounts_file)
                for row in account_reader:
                    if row['ID'] == teacher_id:
                        account_info = row
                        break
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл Accounts.csv не найден.")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при чтении Accounts.csv: {e}")
            return

        # Load teacher info
        try:
            with open("Teachers.csv", newline='', encoding='utf-8') as teachers_file:
                teacher_reader = csv.DictReader(teachers_file)
                for row in teacher_reader:
                    if row['ID_Accounts'] == teacher_id:
                        teacher_info = row
                        break
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл Teachers.csv не найден.")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при чтении Teachers.csv: {e}")
            return

        if account_info and teacher_info:
            self.login_entry.insert(0, account_info['Login'])
            self.password_entry.insert(0, account_info['Password'])
            self.name_entry.insert(0, teacher_info['Name'])
            self.position_entry.insert(0, teacher_info['Position'])
            self.experience_entry.insert(0, teacher_info['Experience'])
            self.degree_entry.insert(0, teacher_info['Degree'])
            self.specialty_entry.insert(0, teacher_info['Specialty'])
        else:
            messagebox.showerror("Ошибка", "Преподаватель не найден.")

    def edit_teacher(self):

        teacher_id = str(self.teacher[2])

        # Get the updated info
        updated_login = self.login_entry.get()
        updated_password = self.password_entry.get()
        updated_name = self.name_entry.get()
        updated_position = self.position_entry.get()
        updated_experience = self.experience_entry.get()
        updated_degree = self.degree_entry.get()
        updated_specialty = self.specialty_entry.get()

        # Update account info
        accounts = []
        try:
            with open("Accounts.csv", newline='', encoding='utf-8') as accounts_file:
                account_reader = csv.DictReader(accounts_file)
                for row in account_reader:
                    if row['ID'] == teacher_id:
                        row['Login'] = updated_login
                        row['Password'] = updated_password
                    accounts.append(row)
            with open("Accounts.csv", 'w', newline='', encoding='utf-8') as accounts_file:
                fieldnames = ['ID', 'Login', 'Password']
                writer = csv.DictWriter(accounts_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(accounts)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл Accounts.csv не найден.")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обновлении Accounts.csv: {e}")
            return

        # Update teacher info
        teachers = []
        try:
            with open("Teachers.csv", newline='', encoding='utf-8') as teachers_file:
                teacher_reader = csv.DictReader(teachers_file)
                for row in teacher_reader:
                    if row['ID_Accounts'] == teacher_id:
                        row['Name'] = updated_name
                        row['Position'] = updated_position
                        row['Experience'] = updated_experience
                        row['Degree'] = updated_degree
                        row['Specialty'] = updated_specialty
                    teachers.append(row)
            with open("Teachers.csv", 'w', newline='', encoding='utf-8') as teachers_file:
                fieldnames = ['ID_Accounts', 'Name', 'Degree', 'Position', 'Experience', 'Specialty']
                writer = csv.DictWriter(teachers_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(teachers)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл Teachers.csv не найден.")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обновлении Teachers.csv: {e}")
            return

        messagebox.showinfo("Успех", "Информация о преподавателе обновлена.")
        self.master.show_teacher_list()
    
    def edit_schedule(self):
        teacher_id = self.teacher[2] 
        self.master.show_discipline_list(teacher_id)