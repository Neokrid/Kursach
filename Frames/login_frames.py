import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Авторизация", font=("Helvetica", 16)).pack(pady=10)
        
        tk.Label(self, text="Логин").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        
        tk.Label(self, text="Пароль").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Label(self, text="Роль").pack(pady=5)
        self.role = tk.StringVar()
        roles = ["Администратор", "Супервайзер", "Преподаватель"]
        self.role_combobox = ttk.Combobox(self, textvariable=self.role, values=roles)
        self.role_combobox.pack(pady=5)

        tk.Button(self, text="Вход", command=self.login).pack(pady=20)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role.get()

        account_id = self.check_account_credentials(username, password)
        if account_id:
            if self.check_role(account_id, role):
                if role == "Администратор":
                    self.master.show_admin_dashboard()
                elif role == "Супервайзер":
                    self.master.show_supervisor_dashboard()
                elif role == "Преподаватель":
                    self.master.show_teacher_dashboard(account_id)
            else:
                messagebox.showerror("Error", "Invalid role for this account")
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def check_account_credentials(self, username, password):
        try:
            with open('Accounts.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Login'] == username and row['Password'] == password:
                        return row['ID']
        except UnicodeDecodeError:
            try:
                with open('Accounts.csv', mode='r', newline='', encoding='ISO-8859-1') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['Login'] == username and row['Password'] == password:
                            return row['ID']
            except FileNotFoundError:
                messagebox.showerror("Error", "Accounts.csv file not found")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts.csv file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return None

    def check_role(self, account_id, role):
        filename = ""
        if role == "Администратор":
            filename = 'Admins.csv'
        elif role == "Преподаватель":
            filename = 'Teachers.csv'
        elif role == "Супервайзер":
            filename = 'Supervisors.csv'
        
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID_Accounts'] == account_id:
                        return True
        except UnicodeDecodeError:
            try:
                with open(filename, mode='r', newline='', encoding='ISO-8859-1') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['ID_Accounts'] == account_id:
                            return True
            except FileNotFoundError:
                messagebox.showerror("Error", f"{filename} file not found")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", f"{filename} file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return False