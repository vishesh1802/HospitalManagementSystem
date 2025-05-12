import csv

def authenticate(username, password, path="Credentials.csv"):
    try:
        with open(path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    return row['role']
    except FileNotFoundError:
        print("Credential file not found.")
    return None
