class Department:
    def __init__(self, name):
        self.name = name
        self.patients = set()

    def add_patient(self, patient):
        self.patients.add(patient)

    def remove_patient(self, patient):
        if patient in self.patients:
            self.patients.remove(patient)
