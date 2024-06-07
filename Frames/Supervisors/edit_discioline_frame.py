import tkinter as tk
import csv
from tkinter import messagebox
from datetime import datetime, timedelta  # Добавляем импорт datetime и timedelta

class EditDisciplineFrame(tk.Frame):
    def __init__(self, master, discipline, teacher_id):
        super().__init__(master)
        self.master = master
        self.discipline = discipline
        self.teacher_id = teacher_id
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Редактировать дисциплину", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self, text="Дисциплина:").pack(pady=5)
        self.discipline_entry = tk.Entry(self)
        self.discipline_entry.pack(pady=5)
        self.discipline_entry.insert(0, self.discipline['Names'])

        tk.Label(self, text="Группа:").pack(pady=5)
        self.group_entry = tk.Entry(self)
        self.group_entry.pack(pady=5)
        self.group_entry.insert(0, self.discipline['Group'])

        tk.Label(self, text="Тип занятия:").pack(pady=5)
        self.type_entry = tk.Entry(self)
        self.type_entry.pack(pady=5)
        self.type_entry.insert(0, self.discipline['Type'])

        tk.Label(self, text="Дата начала:").pack(pady=5)
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.pack(pady=5)
        self.start_date_entry.insert(0, self.discipline['Start Time'])
        
        tk.Label(self, text="Дата завершения:").pack(pady=5)
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.pack(pady=5)
        self.end_date_entry.insert(0, self.discipline['End Time'])

        tk.Button(self, text="Подтвердить", command=self.save_discipline).pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Button(self, text="Назад", command=lambda: self.master.show_discipline_list(self.teacher_id)).pack(side=tk.LEFT, padx=10, pady=10)

    def calculate_hours(self, start_time, end_time):
        start_date = datetime.strptime(start_time, '%d-%m-%Y')
        end_date = datetime.strptime(end_time, '%d-%m-%Y')
        
        weekdays = 0
        current_day = start_date
        while current_day <= end_date:
            if current_day.weekday() < 5:  # Monday to Friday are 0-4
                weekdays += 1
            current_day += timedelta(days=1)
        
        hours = weekdays * 4
        return hours

    def save_discipline(self):
        updated_discipline = {
            'ID': self.discipline['ID'],
            'ID_Accounts': self.discipline['ID_Accounts'],
            'Names': self.discipline_entry.get(),
            'Start Time': self.start_date_entry.get(),
            'End Time': self.end_date_entry.get(),
            'Type': self.type_entry.get()
        }

        updated_group = self.group_entry.get()

        try:
            with open('Disciplines.csv', 'r', newline='', encoding='utf-8') as file:
                reader = list(csv.DictReader(file))
                for i, row in enumerate(reader):
                    if row['ID'] == self.discipline['ID']:
                        reader[i] = updated_discipline
                        break

            with open('Disciplines.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=reader[0].keys())
                writer.writeheader()
                writer.writerows(reader)

            with open('DisciplinesToGroups.csv', 'r', newline='', encoding='utf-8') as file:
                reader = list(csv.DictReader(file))
                for i, row in enumerate(reader):
                    if row['ID_Disciplines'] == self.discipline['ID']:
                        reader[i]['Group'] = updated_group
                        break

            with open('DisciplinesToGroups.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=reader[0].keys())
                writer.writeheader()
                writer.writerows(reader)

            messagebox.showinfo("Success", "Дисциплина успешно обновлена.")
            self.master.show_discipline_list(self.teacher_id)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
