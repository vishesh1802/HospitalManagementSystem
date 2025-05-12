class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def can_perform(self, action):
        permissions = {
            'admin': ['count_visits'],
            'clinician': ['add_patient', 'remove_patient', 'retrieve_patient', 'view_note', 'count_visits'],
            'nurse': ['add_patient', 'remove_patient', 'retrieve_patient', 'view_note', 'count_visits'],
            'management': ['generate_statistics']
        }
        return action in permissions.get(self.role, [])
