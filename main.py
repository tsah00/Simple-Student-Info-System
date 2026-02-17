import csv
import os

class SimpleSIS:
    def __init__(self):
        self.files = {
            'college': 'colleges.csv',
            'program': 'programs.csv',
            'student': 'students.csv'
        }
        self.headers = {
            'college': ['code', 'name'],
            'program': ['code', 'name', 'college_code'],
            'student': ['id', 'firstname', 'lastname', 'program_code', 'year', 'gender']
        }
        self._initialize_files()

    def _initialize_files(self):
        """Creates the CSV files with headers if they don't exist."""
        for key, filename in self.files.items():
            if not os.path.exists(filename):
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.headers[key])

    def _read_data(self, key):
        with open(self.files[key], 'r', newline='') as f:
            return list(csv.DictReader(f))

    def _write_data(self, key, data):
        with open(self.files[key], 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers[key])
            writer.writeheader()
            writer.writerows(data)

    def create(self, entity, data):
        """Adds a new record. Checks for ID uniqueness."""
        current_data = self._read_data(entity)
        pk = self.headers[entity][0] # First column is usually the ID/Code
        
        if any(row[pk] == data[pk] for row in current_data):
            print(f"Error: Record with {pk} {data[pk]} already exists.")
            return False
        
        current_data.append(data)
        self._write_data(entity, current_data)
        print(f"{entity.capitalize()} added successfully.")

    def list_all(self, entity, sort_by=None):
        data = self._read_data(entity)
        if sort_by:
            data.sort(key=lambda x: x.get(sort_by, ''))
        return data

    def search(self, entity, field, value):
        data = self._read_data(entity)
        return [row for row in data if value.lower() in row.get(field, '').lower()]

    def update(self, entity, pk_value, new_data):
        data = self._read_data(entity)
        pk = self.headers[entity][0]
        updated = False
        for row in data:
            if row[pk] == pk_value:
                row.update(new_data)
                updated = True
        if updated:
            self._write_data(entity, data)
            print("Update successful.")
        else:
            print("Record not found.")

    def delete(self, entity, pk_value):
        data = self._read_data(entity)
        pk = self.headers[entity][0]
        new_data = [row for row in data if row[pk] != pk_value]
        if len(new_data) < len(data):
            self._write_data(entity, new_data)
            print("Deletion successful.")
        else:
            print("Record not found.")

sis = SimpleSIS()

sis.create('college', {'code': 'CCS', 'name': 'College of Computer Studies'})
sis.create('program', {'code': 'BSCS', 'name': 'Bachelor of Science in Computer Science', 'college_code': 'CCS'})
sis.create('student', {
    'id': '2023-4004', 
    'firstname': 'Cha Jane', 
    'lastname': 'Torres', 
    'program_code': 'BSCS', 
    'year': '2', 
    'gender': 'Female'
})

print("\nSorted Student List:")
for s in sis.list_all('student', sort_by='lastname'):
    print(f"{s['id']}: {s['lastname']}, {s['firstname']}")

print("\nSearch Result (Firstname 'Cha'):")
print(sis.search('student', 'firstname', 'Cha'))