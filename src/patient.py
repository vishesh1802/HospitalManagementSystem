class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.visits = []
        self.notes = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def add_note(self, note):
        self.notes.append(note)
