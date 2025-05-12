# HospitalManagementSystem

This project implements Role-Based Patient Management System for a hospital.

The features includes:

User Authentication for admin, management, clinician, nurse using username and passoword.

CRUD operations on patient records: retrieve, add, remove.

Clinical note viewing by date.

Visit statistics generation.

Tkinter GUI for interactive use.

Usage logging tracking user actions.

Repository Structure
``` 
├── data/
│   ├── PA3_data.csv         # Patient and visit data
│   ├── PA3_Notes.csv        # Clinical notes data
│   └── PA3_credentials.csv  # User credentials and roles
├── output/
│   ├── visit_stats.png
│   ├── visits_monthly_trend.png
│   └── output.txt           # Example retrieve_patient output
├── src/
│   ├── patient_management.py        # Core backend classes
│   ├── ui_patient_management.py     # Tkinter GUI launcher
│   ├── patient.py
│   ├── visit.py
│   ├── department.py
│   └── note.py
├── UML_Diagram.png          # UML class diagram
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

Steps to run the code

1. Clone the Repository


2. Set up the Python Environment
   ``` bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the GUI
   ```bash
   python src/ui_patient_management.py
   ```

4. Interact with the login screen

    Enter username and password from data/Credentials.csv.

    Use role-based buttons.

    View results in pop-up windows and consult usage_log.csv for action logs.


Project Description:

  Authentication: Validates credentials against Credentials.csv, loading role-specific UI.

  Data Loading: Parses Patient_data.csv, normalizes dates, safely handles missing/invalid age.

  CRUD Operations:

    Retrieve: Writes patient summary to output/output.txt and displays.

    Add: Gathers fields via GUI, appends to CSV and memory.

    Remove: Deletes patient records and rewrites CSV.

  Notes: Views clinical notes for a given patient and date.

  Statistics: Generates statistics for specific user.

  Logging: Appends user actions to output/usage_log.csv.
