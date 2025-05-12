
import datetime
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
from patient_management import PatientManagementSystem

class PatientManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Management Login")
        self.credentials = self.load_credentials("Credentials.csv")
        self.system = None
        self.username = None
        self.login_time = None
        self.role = None
        self.init_login()

    def load_credentials(self, path):
        creds = {}
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                creds[row['username']] = (row['password'], row['role'])
        return creds

    def init_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Login", command=self.validate_login).grid(row=2, columnspan=2)

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username in self.credentials and self.credentials[username][0] == password:
            self.username = username
            self.login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.role = self.credentials[username][1]
            self.system = PatientManagementSystem("Patient_data.csv")
            self.system.load_notes("Notes.csv")
            self.show_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.role in ("admin", "management"):
            actions = ["Generate Statistics", "Count Visits", "Exit"]
        else:
            actions = ["Retrieve Patient", "Add Patient", "Remove Patient", "Count Visits", "View Note", "Exit"]
        for action in actions:
            tk.Button(self.root, text=action, width=25,
                      command=lambda a=action: self.execute_action(a)).pack(pady=5)

    def log_action(self, action_name):
        log_file = "usage_log.csv"
        headers = ["Username", "Role", "Action", "Login Time", "Action Time"]
        action_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [self.username, self.role, action_name, self.login_time, action_time]
        write_header = not os.path.exists(log_file)
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(headers)
            writer.writerow(row)

    def display_result(self, text):
        w = tk.Toplevel(self.root)
        w.title("Result")
        box = tk.Text(w, wrap="word", height=20, width=70)
        box.insert("1.0", text)
        box.config(state="disabled")
        box.pack(padx=10, pady=10)

    def execute_action(self, action):
        self.log_action(action)
        if action == "Exit":
            self.root.quit()

        elif action == "Generate Statistics":
            self.system.generate_statistics()
            self.display_result("Statistics chart saved to visit_stats.png")

        elif action == "Count Visits":
            date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD):")
            if not date:
                return
            try:
                dt = datetime.datetime.strptime(date.strip(), "%Y-%m-%d")
            except ValueError:
                dt = datetime.datetime.strptime(date.strip(), "%m/%d/%Y")
            date_str = dt.strftime("%Y-%m-%d")
            count = self.system.review_date(date_str) or 0
            self.display_result(f"Total visits on {date_str}: {count}")

        elif action == "Retrieve Patient":
            pid = simpledialog.askstring("Retrieve", "Enter Patient ID:")
            if not pid:
                return
            out = "output.txt"
            ok = self.system.retrieve_patient(pid, out)
            data = open(out).read() if ok else f"Patient {pid} not found."
            self.display_result(data)

        elif action == "Add Patient":
            pid = simpledialog.askstring("Add Patient", "Enter Patient ID:")
            if not pid:
                return
            vt = simpledialog.askstring("Add Patient", "Enter Visit Date (YYYY-MM-DD):")
            dept = simpledialog.askstring("Add Patient", "Enter Department:")
            gender = simpledialog.askstring("Add Patient", "Enter Gender:")
            race = simpledialog.askstring("Add Patient", "Enter Race:")
            age = simpledialog.askinteger("Add Patient", "Enter Age:")
            ethnicity = simpledialog.askstring("Add Patient", "Enter Ethnicity:")
            insurance = simpledialog.askstring("Add Patient", "Enter Insurance:")
            zip_code = simpledialog.askstring("Add Patient", "Enter Zip Code:")
            complaint = simpledialog.askstring("Add Patient", "Enter Chief Complaint:")

            try:
                datetime.datetime.strptime(vt.strip(), "%Y-%m-%d")
            except:
                self.display_result("Invalid date. Use YYYY-MM-DD.")
                return

            self.system.add_visit_gui(
                pid, vt.strip(), dept.strip(), gender.strip(),
                race.strip(), age, ethnicity.strip(),
                insurance.strip(), zip_code.strip(), complaint.strip()
            )
            self.display_result(f"Added visit for {pid} on {vt}.")

        elif action == "Remove Patient":
            pid = simpledialog.askstring("Remove", "Enter Patient ID:")
            if not pid:
                return
            self.system.remove_patient(pid)
            self.display_result(f"Removed patient {pid}.")

        elif action == "View Note":
            pid = simpledialog.askstring("View Note", "Enter Patient ID:")
            date = simpledialog.askstring("View Note", "Enter Date (YYYY-MM-DD):")
            if not pid or not date:
                return
            try:
                dt = datetime.datetime.strptime(date.strip(), "%Y-%m-%d")
            except ValueError:
                dt = datetime.datetime.strptime(date.strip(), "%m/%d/%Y")
            ds = dt.strftime("%Y-%m-%d")
            note = self.system.view_note(pid, ds)
            self.display_result(note or f"No notes on {ds} for {pid}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientManagementApp(root)
    root.mainloop()
