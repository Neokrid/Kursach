import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class TeacherListFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Список преподавателей", font=("Helvetica", 16)).pack(pady=10)
        
        columns = ("№", "ФИО", "ID_Accounts")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=5, fill=tk.BOTH, expand=True)

        tk.Button(self, text="Подробности", command=self.show_details).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Добавить преподавателя", command=self.master.show_add_teacher).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Удалить преподавателя", command=self.delete_teacher).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Назад", command=self.master.show_supervisor_dashboard).pack(side=tk.LEFT, padx=10, pady=10)

        self.load_teachers()

    def load_teachers(self):
    
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open("Teachers.csv", newline='', encoding='utf-8') as teachers_file:
                reader = csv.DictReader(teachers_file)
                for i, row in enumerate(reader, start=1):
                    teacher_id, name = row['ID_Accounts'], row['Name']
                    self.tree.insert('', tk.END, values=(i, name, teacher_id))
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл Teachers.csv не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def show_details(self):
        selected_item = self.tree.selection()
        if selected_item:
            teacher = self.tree.item(selected_item)["values"]
            self.master.show_teacher_info(teacher)

    def delete_teacher(self):
        selected_item = self.tree.selection()
        if selected_item:
            teacher = self.tree.item(selected_item)['values']
            teacher_id = str(teacher[2])

            # Delete from tree view
            self.tree.delete(selected_item)

            # Delete from CSV files
            self.delete_teacher_from_files(teacher_id)

    def delete_teacher_from_files(self, teacher_id):
        teachers = []
        accounts = []
        user_found = False

        try:
            # Load and filter Teachers.csv
            with open("Teachers.csv", newline='', encoding='utf-8') as teachers_file:
                teacher_reader = csv.DictReader(teachers_file)
                for row in teacher_reader:
                    if row['ID_Accounts'] != teacher_id:
                        teachers.append(row)
                    else:
                        user_found = True
                        print(f"Found and removing teacher with ID: {teacher_id}")

            # Write updated teachers back to Teachers.csv
            if user_found:
                with open("Teachers.csv", 'w', newline='', encoding='utf-8') as teachers_file:
                    fieldnames = ['ID_Accounts', 'Name', 'Degree', 'Position', 'Experience', 'Specialty']
                    writer = csv.DictWriter(teachers_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(teachers)
            else:
                print(f"Teacher ID {teacher_id} not found in Teachers.csv")

            # Load and filter Accounts.csv
            with open("Accounts.csv", newline='', encoding='utf-8') as accounts_file:
                account_reader = csv.DictReader(accounts_file)
                for row in account_reader:
                    if row['ID'] != teacher_id:
                        accounts.append(row)

            # Write updated accounts back to Accounts.csv
            with open("Accounts.csv", 'w', newline='', encoding='utf-8') as accounts_file:
                fieldnames = ['ID', 'Login', 'Password']
                writer = csv.DictWriter(accounts_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(accounts)

            if user_found:
                messagebox.showinfo("Успех", "Преподаватель успешно удален.")
            else:
                messagebox.showerror("Ошибка", "Преподаватель не найден в файле Teachers.csv.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")