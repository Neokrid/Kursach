import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from datetime import datetime, timedelta

class DisciplineListFrame(tk.Frame):
    def __init__(self, master, teacher_id):
        super().__init__(master)
        self.master = master
        self.teacher_id = teacher_id
        self.create_widgets()
        self.disciplines = []
        self.load_disciplines()

    def create_widgets(self):
        tk.Label(self, text="Список дисциплин", font=("Helvetica", 16)).pack(pady=10)

        columns = ("ID", "Названия", "Группа", "Тип занятия", "Количество часов")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=5, fill=tk.BOTH, expand=True)

        tk.Button(self, text="Редактировать", command=self.edit_discipline).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Узнать подробности", command=self.show_details).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Назад", command=self.master.show_teacher_list).pack(side=tk.LEFT, padx=10, pady=10)

    def load_disciplines(self):
        try:
            with open("Disciplines.csv", newline='', encoding='utf-8') as disciplines_file:
                discipline_reader = csv.DictReader(disciplines_file)
                all_disciplines = list(discipline_reader)

                with open("DisciplinesToGroups.csv", newline='', encoding='utf-8') as groups_file:
                    group_reader = csv.DictReader(groups_file)
                    group_mapping = {row['ID_Disciplines']: row['Group'] for row in group_reader}

                for row in all_disciplines:
                    if row['ID_Accounts'] == str(self.teacher_id):
                        row['Group'] = group_mapping.get(row['ID'], 'N/A')
                        row['Hours'] = self.calculate_hours(row['Start Time'], row['End Time'])
                        self.disciplines.append(row)
                        self.tree.insert('', tk.END, values=(row['ID'], row['Names'], row['Group'], row['Type'], row['Hours']))
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Disciplines file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

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

    def edit_discipline(self):
        selected_item = self.tree.selection()
        if selected_item:
            id = self.tree.item(selected_item)['values'][0]
            for discipline in self.disciplines:
                if int(discipline['ID']) == id:
                    self.master.show_edit_discipline(discipline, self.teacher_id)
                    break

    def show_details(self):
        selected_item = self.tree.selection()
        if selected_item:
            subject_details = self.tree.item(selected_item)['values']
            self.master.show_group_list(subject_details, self.teacher_id)  # Передача teacher_id