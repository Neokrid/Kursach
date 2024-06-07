import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

class ManageUsersFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        tk.Label(self, text="Список пользователей", font=("Helvetica", 16)).pack(pady=10)
        columns = ("ID","Имя", "Логин", "Пароль", "Роль", "Группа")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=5, fill=tk.BOTH, expand=True)

        tk.Button(self, text="Назад", command=self.master.show_admin_dashboard).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Удалить пользователя", command=self.delete_user).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Добавить пользователя", command=self.master.show_add_user).pack(side=tk.LEFT, padx=10, pady=10)

    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        users = self.read_users_from_files()
        for user in users:
            self.tree.insert('', tk.END, values=user)

    def read_users_from_files(self):
        users = []
        accounts = {}

        try:
            with open("Accounts.csv", newline='', encoding='utf-8') as accounts_file:
                account_reader = csv.DictReader(accounts_file)
                accounts = {row['ID']: row for row in account_reader}

            role_files = [
                ("Преподаватель", "Teachers.csv"),
                ("Администратор", "Admins.csv"),
                ("Супервайзер", "Supervisors.csv")
            ]

            for role, file in role_files:
                try:
                    with open(file, newline='', encoding='utf-8') as role_file:
                        role_reader = csv.DictReader(role_file)
                        for row in role_reader:
                            account_id = row['ID_Accounts'].strip()
                            if account_id in accounts:
                                account = accounts[account_id]
                                full_name = row['Name'].strip()
                                username = account['Login'].strip()
                                password = account['Password'].strip()
                                users.append((account_id,full_name, username, password, role, ''))
                except FileNotFoundError:
                    continue  # Skip if file does not exist

            # Теперь загрузим студентов
            try:
                with open("Students.csv", newline='', encoding='utf-8') as students_file:
                    student_reader = csv.DictReader(students_file)
                    for row in student_reader:
                        full_name = row['Name'].strip()
                        username = row['ID_Accounts'].strip()
                        password = ''  # Пароль не нужен для студентов, так как они не в Accounts.csv
                        group = row['Group'].strip()
                        users.append((full_name, username, password, "Студент", group))
            except FileNotFoundError:
                messagebox.showerror("Error", "Students file not found")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading students: {e}")

        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        return users

    def delete_user(self):
        selected_item = self.tree.selection()
        if selected_item:
            user = self.tree.item(selected_item)['values']
            id = user[0]
            role = user[4]

            if role == "Администратор":
                messagebox.showerror("Error", "You cannot delete an administrator")
                return

            # Delete from tree view
            self.tree.delete(selected_item)
            print(user)
            # Delete from CSV files
            self.delete_user_from_files(id, role)

    def delete_user_from_files(self, id_to_delete, role):
        accounts = []
        deleted_account_id = None
        user_found_in_role = False

        try:
            print(f"Attempting to delete user: {id_to_delete} with role: {role}")

            # Load and filter Accounts.csv, only if the role is not "Студент"
            if role != "Студент":
                with open("Accounts.csv", newline='', encoding='utf-8') as accounts_file:
                    account_reader = csv.DictReader(accounts_file)
                    for row in account_reader:
                        if str(row['ID']).strip() == str(id_to_delete):
                            deleted_account_id = row['ID'].strip()
                            print(f"Found user in Accounts.csv with ID: {deleted_account_id}")
                        else:
                            accounts.append(row)

                if deleted_account_id:
                    # Write updated accounts back to Accounts.csv
                    with open("Accounts.csv", 'w', newline='', encoding='utf-8') as accounts_file:
                        fieldnames = ['ID', 'Login', 'Password']
                        writer = csv.DictWriter(accounts_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(accounts)

            # Remove from role files based on the role
            role_files = {
                "Преподаватель": "Teachers.csv",
                "Администратор": "Admins.csv",
                "Супервайзер": "Supervisors.csv",
                "Студент": "Students.csv"
            }

            role_file_path = role_files.get(role)
            if role_file_path:
                roles_data = []
                try:
                    with open(role_file_path, newline='', encoding='utf-8') as role_file:
                        role_reader = csv.DictReader(role_file)
                        for row in role_reader:
                            row_id_accounts = row['ID_Accounts'].strip()
                            id_to_delete_str = str(id_to_delete).strip()  # Приведение к строке
                            print(f"Checking student: {row_id_accounts}, ID to delete: {id_to_delete_str}")
                            print(f"Row data: {row}")

                            if row_id_accounts != id_to_delete_str:
                                roles_data.append(row)
                            else:
                                user_found_in_role = True
                                print(f"Found user in {role_file_path} with ID_Accounts: {id_to_delete_str}")

                    print(f"user_found_in_role: {user_found_in_role}")

                    if user_found_in_role:
                        with open(role_file_path, 'w', newline='', encoding='utf-8') as role_file:
                            fieldnames = role_reader.fieldnames
                            writer = csv.DictWriter(role_file, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(roles_data)
                        print(f"User deleted from {role_file_path}")
                        messagebox.showinfo("Success", "User deleted successfully")
                    else:
                        print(f"User not found in {role_file_path}")
                        messagebox.showerror("Error", "User not found in role files")
                except FileNotFoundError:
                    messagebox.showerror("Error", f"{role_file_path} not found")

            self.load_users()  # Обновить список пользователей в Treeview

        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_user_list(self):
        self.load_users()