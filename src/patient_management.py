
from calendar import month
import csv
import datetime
import os
from collections import defaultdict
from turtle import pd
import matplotlib.pyplot as plt  # type: ignore
from note import Note
from department import Department
from visit import Visit
from patient import Patient
import uuid

class PatientManagementSystem:
    def __init__(self, input_path):
        self.input_path = input_path
        self.patients = {}
        self.departments = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.input_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pid = row['Patient_ID'].strip()
                    if pid not in self.patients:
                        self.patients[pid] = Patient(pid)

                    dept = row['Visit_department'].strip()
                    if dept not in self.departments:
                        self.departments[dept] = Department(dept)

                    # Parse and normalize date
                    raw_time = row['Visit_time'].strip()
                    try:
                        visit_date = self._parse_date(raw_time)
                    except ValueError:
                        print(f"Warning: Unknown date format: {raw_time}")
                        continue

                    visit = Visit(
                        visit_id=row['Visit_ID'].strip(),
                        visit_time=visit_date.isoformat(),
                        department=self.departments[dept],
                        gender=row['Gender'].strip(),
                        race=row['Race'].strip(),
                        age=self._safe_int(row['Age'].strip(), pid),
                        ethnicity=row['Ethnicity'].strip(),
                        insurance=row['Insurance'].strip(),
                        zip_code=row['Zip_code'].strip(),
                        chief_complaint=row['Chief_complaint'].strip()
                    )
                    if visit.age is None:
                        continue  # skip if age invalid

                    self.patients[pid].add_visit(visit)
                    self.departments[dept].add_patient(self.patients[pid])
        except FileNotFoundError:
            print("Error: Data file not found.")

    def _safe_int(self, s, pid):
        try:
            return int(s)
        except ValueError:
            print(f"Warning: invalid age '{s}' for patient {pid}; skipping record.")
            return None

    def load_notes(self, note_file_path):
        try:
            with open(note_file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pid = row['Patient_ID'].strip()
                    if pid in self.patients:
                        note = Note(
                            note_id=row['Note_ID'].strip(),
                            visit_id=row['Visit_ID'].strip(),
                            note_text=row['Note_text'].strip()
                        )
                        self.patients[pid].add_note(note)
        except Exception as e:
            print(f"Error loading notes: {e}")

    def _parse_date(self, s: str) -> datetime.date:
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%m-%d-%Y"):
            try:
                return datetime.datetime.strptime(s.strip(), fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Unknown date format: {s!r}")

    def review_date(self, date_str: str) -> int | None:
        try:
            target = self._parse_date(date_str)
        except ValueError:
            return None

        count = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                try:
                    vt = self._parse_date(visit.visit_time)
                except ValueError:
                    continue
                if vt == target:
                    count += 1
        return count

    def view_note(self, patient_id: str, date_str: str) -> str | None:
        if patient_id not in self.patients:
            return None
        try:
            target = self._parse_date(date_str)
        except ValueError:
            return None

        results = []
        for visit in self.patients[patient_id].visits:
            try:
                vt = self._parse_date(visit.visit_time)
            except ValueError:
                continue
            if vt == target:
                for note in self.patients[patient_id].notes:
                    if note.visit_id == visit.visit_id:
                        results.append(f"Note ID: {note.note_id}\n{note.note_text}")
        return "\n\n".join(results) if results else None

    def retrieve_patient(self, patient_id: str, output_file: str) -> bool:
        if patient_id not in self.patients:
            return False
        patient = self.patients[patient_id]
        try:
            with open(output_file, 'w') as f:
                f.write(f"Patient ID: {patient.patient_id}\n")
                for visit in patient.visits:
                    f.write(f"Visit ID: {visit.visit_id}, Date: {visit.visit_time}, Dept: {visit.department.name}\n")
                for note in patient.notes:
                    f.write(f"Note ID: {note.note_id}, Text: {note.note_text}\n")
            return True
        except:
            return False

    def add_visit_gui(self,
                      patient_id, visit_time, dept_name, gender, race,
                      age, ethnicity, insurance, zip_code, complaint,note_id=None, note_type=None, note_text=""):
        pid = patient_id.strip()
        if pid not in self.patients:
            self.patients[pid] = Patient(pid)
        if dept_name not in self.departments:
            self.departments[dept_name] = Department(dept_name)

        # Create visit
        visit = Visit(
            visit_id=str(uuid.uuid4())[:8],
            visit_time=visit_time,
            department=self.departments[dept_name],
            gender=gender, race=race, age=int(age),
            ethnicity=ethnicity, insurance=insurance,
            zip_code=zip_code, chief_complaint=complaint
        )

        self.patients[pid].add_visit(visit)
        self.departments[dept_name].add_patient(self.patients[pid])
        # Add note if provided
        if note_id and note_text:
            note = Note(note_id=note_id, visit_id=visit.visit_id, note_text=note_text)
            note.note_type = note_type  
            self.patients[pid].add_note(note)

        fieldnames = [
            'Patient_ID','Visit_ID','Visit_time','Visit_department',
            'Race','Gender','Ethnicity','Age',
            'Zip_code','Insurance','Chief_complaint', 'Note_ID', 'Note_type'
        ]
        with open(self.input_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({
                'Patient_ID': pid,
                'Visit_ID': visit.visit_id,
                'Visit_time': visit_time,
                'Visit_department': dept_name,
                'Race': race,
                'Gender': gender,
                'Ethnicity': ethnicity,
                'Age': age,
                'Zip_code': zip_code,
                'Insurance': insurance,
                'Chief_complaint': complaint,
                'Note_ID': note_id if note_id else "",
                'Note_type': note_type if note_type else ""
            })

    def remove_patient(self, patient_id: str):
        pid = patient_id.strip()
        if pid in self.patients:
            del self.patients[pid]
        # rewrite CSV without this patient
        with open(self.input_path, 'r', newline='') as f:
            rows = list(csv.DictReader(f))
        with open(self.input_path, 'w', newline='') as f:
            fieldnames = rows[0].keys() if rows else []
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row['Patient_ID'].strip() != pid:
                    writer.writerow(row)

    def generate_statistics(self):
        from collections import Counter
        import matplotlib.pyplot as plt
        from datetime import datetime

        # Aggregate data
        date_counter = Counter()
        insurance_counter = Counter()
        gender_counter = Counter()
        department_counter = Counter()
        complaint_counter = Counter()
        age_groups = {"Child": 0, "Adult": 0, "Senior": 0}

        def age_group(a):
            return "Child" if a < 18 else "Adult" if a < 65 else "Senior"

        for patient in self.patients.values():
            for visit in patient.visits:
                try:
                    datetime.strptime(visit.visit_time.strip(), "%Y-%m-%d")
                except ValueError:
                    continue

                date_counter[visit.visit_time] += 1
                insurance_counter[visit.insurance] += 1
                gender_counter[visit.gender] += 1
                department_counter[visit.department.name] += 1
                complaint_counter[visit.chief_complaint.lower()] += 1
                age_groups[age_group(visit.age)] += 1

        # Build a 2x2 figure
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Hospital Visit Statistics", fontsize=18)

        # 1) Department Distribution [0,0]
        if department_counter:
            labels_dept, vals_dept = zip(*sorted(department_counter.items(), key=lambda x: x[1], reverse=True))
            axs[0, 0].barh(labels_dept, vals_dept, color="mediumslateblue")
            axs[0, 0].set_title("Department Visit Frequency")
            axs[0, 0].set_xlabel("Number of Visits")
            axs[0, 0].invert_yaxis()
            axs[0, 0].grid(axis="x", linestyle="--", alpha=0.5)

        # 2) Insurance Distribution as Donut [0,1]
        if insurance_counter:
            labels_ins, vals_ins = zip(*insurance_counter.items())
            wedges, texts, autotexts = axs[0, 1].pie(vals_ins, labels=labels_ins, autopct="%1.1f%%", startangle=140)
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            axs[0, 1].add_artist(centre_circle)
            axs[0, 1].set_title("Insurance Distribution (Donut)")

        # 3) Gender Distribution [1,0]
        if gender_counter:
            labels_gen, vals_gen = zip(*gender_counter.items())
            axs[1, 0].bar(labels_gen, vals_gen, color="orange")
            axs[1, 0].set_title("Gender Distribution")
            axs[1, 0].set_ylabel("Count")
            axs[1, 0].grid(axis="y", linestyle="--", alpha=0.5)

        # 4) Age Group Distribution [1,1]
        if age_groups:
            labels_age, vals_age = zip(*age_groups.items())
            axs[1, 1].bar(labels_age, vals_age, color="seagreen")
            axs[1, 1].set_title("Age Group Distribution")
            axs[1, 1].grid(axis="y", linestyle="--", alpha=0.5)

        # Final layout and save
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig("output/visit_stats.png")
        plt.close(fig)

        print("Chart saved to output/visit_stats.png.")

