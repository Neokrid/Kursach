import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class GroupListFrame(tk.Frame):
    def __init__(self, master, subject_details, teacher_id):
        super().__init__(master)
        self.master = master
        self.subject_details = subject_details
        self.teacher_id = teacher_id  # Добавление teacher_id
        self.create_widgets()
        self.load_group_members()

    def create_widgets(self):
        tk.Label(self, text=f"Список группы для дисциплины {self.subject_details[1]}", font=("Helvetica", 16)).pack(pady=10)

        columns = ("№", "ФИО")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=5, fill=tk.BOTH, expand=True)

        tk.Button(self, text="Назад", command=lambda: self.master.show_discipline_list(self.teacher_id)).pack(pady=5)

    def load_group_members(self):
        discipline_id = str(self.subject_details[0])
        group = self.get_group_by_discipline(discipline_id)
        if group:
            students = self.get_students_by_group(group)
            for idx, student in enumerate(students, start=1):
                self.tree.insert('', tk.END, values=(idx, student[1]))
        else:
            messagebox.showinfo("Info", "No group found for this discipline")

    def get_group_by_discipline(self, discipline_id):
        group = None
        try:
            with open("DisciplinesToGroups.csv", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['ID_Disciplines'] == discipline_id:
                        group = row['Group']
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "DisciplinesToGroups file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return group

    def get_students_by_group(self, group):
        students = []
        try:
            with open("Students.csv", newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Group'] == group:
                        students.append((row['ID_Accounts'], row['Name']))
                        print(f"Найден студент: ID={row['ID_Accounts']}, ФИО={row['Name']}")  # Вывод информации о найденных студентах
        except FileNotFoundError:
            messagebox.showerror("Error", "Students file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return students
    