# main.py
import argparse
from user import User
from utils import authenticate
from patient_management import PatientManagementSystem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-username", required=True)
    parser.add_argument("-password", required=True)
    args = parser.parse_args()

    role = authenticate(args.username, args.password)
    if not role:
        print("Invalid credentials. Access denied.")
        return

    user = User(args.username, role)
    system = PatientManagementSystem("Patient_data.csv")
    system.load_notes("Notes.csv")

    if role == "admin":
        date = input("Enter date (YYYY-MM-DD) to count visits: ")
        system.review_date(date)

    elif role == "management":
        system.generate_statistics()

    elif role in ("nurse", "clinician"):
        while True:
            action = input("Enter action (add_patient, remove_patient, retrieve_patient, view_note, count_visits, Stop): ")
            if action == "Stop":
                break
            elif not user.can_perform(action):
                print(f"Action {action} not permitted for your role.")
                continue
            if action == "add_patient":
                pid = input("Enter Patient ID: ")
                system.add_visit(pid)
            elif action == "remove_patient":
                pid = input("Enter Patient ID: ")
                system.remove_patient(pid)
            elif action == "retrieve_patient":
                pid = input("Enter Patient ID: ")
                system.retrieve_patient(pid, "output.txt")
            elif action == "count_visits":
                date = input("Enter date (YYYY-MM-DD): ")
                system.review_date(date)
            elif action == "view_note":
                pid = input("Enter Patient ID: ")
                date = input("Enter Date (YYYY-MM-DD): ")
                system.view_note(pid, date)


if __name__ == "__main__":
    main()
