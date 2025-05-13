import tkinter as tk
from ui_patient_management import PatientManagementApp

def main():
    root = tk.Tk()
    app = PatientManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
