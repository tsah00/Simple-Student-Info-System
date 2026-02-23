import csv
import os

class SimpleSIS:
    def __init__(self):
        self.files = {
            'College': 'colleges.csv',
            'Program': 'programs.csv',
            'Student': 'students.csv'
        }
        self.headers = {
            'College': ['Code', 'Name'],
            'Program': ['Code', 'Name', 'College_Code'],
            'Student': ['ID', 'Firstname', 'Lastname', 'Program_Code', 'Year', 'Gender']
        }
        self._initialize_files()

    def _initialize_files(self):
        """Creates CSV files with headers if they don't exist."""
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

    # --- CRUDL Operations ---

    def create(self, entity, data):
        current_data = self._read_data(entity)
        pk = self.headers[entity][0]
        
        # Check if Primary Key already exists (Case-insensitive)
        if any(row[pk].lower() == data[pk].lower() for row in current_data):
            print(f"\n[!] Error: {pk} '{data[pk]}' already exists.")
            return False
        
        # Referential Integrity Check: Student must belong to an existing Program
        if entity == 'Student':
            programs = self._read_data('Program')
            if not any(p['Code'].lower() == data['Program_Code'].lower() for p in programs):
                print(f"\n[!] Error: Program Code '{data['Program_Code']}' Does not exist.")
                return False

        current_data.append(data)
        self._write_data(entity, current_data)
        print(f"\n[+] {entity.capitalize()} added successfully.")
        return True

    def list_all(self, entity, sort_by=None):
        data = self._read_data(entity)
        if sort_by and sort_by in self.headers[entity]:
            data.sort(key=lambda x: x.get(sort_by, '').lower())
        return data

    def search(self, entity, field, value):
        data = self._read_data(entity)
        return [row for row in data if value.lower() in row.get(field, '').lower()]

    def update(self, entity, pk_value, new_data):
        data = self._read_data(entity)
        pk = self.headers[entity][0]
        updated = False
        for row in data:
            if row[pk].lower() == pk_value.lower():
                row.update({k: v for k, v in new_data.items() if v}) # Only update non-empty fields
                updated = True
        if updated:
            self._write_data(entity, data)
            print("\n[+] Update successful.")
        else:
            print("\n[!] Record not found.")
        return updated

    def delete(self, entity, pk_value):
        data = self._read_data(entity)
        pk = self.headers[entity][0]
        initial_count = len(data)
        data = [row for row in data if row[pk].lower() != pk_value.lower()]
        
        if len(data) < initial_count:
            self._write_data(entity, data)
            print("\n[-] Deletion successful.")
            return True
        print("\n[!] Record not found.")
        return False

# --- UI Helper Functions ---

def print_table(data, headers):
    if not data:
        print("\n(No records found)")
        return
    print("\n" + " | ".join([h.upper().ljust(15) for h in headers]))
    print("-" * (len(headers) * 18))
    for row in data:
        print(" | ".join([str(row[h]).ljust(15) for h in headers]))

def main_menu():
    sis = SimpleSIS()
    while True:
        print("\n=== STUDENT INFORMATION SYSTEM ===")
        print("1. Colleges")
        print("2. Programs")
        print("3. Students")
        print("4. Exit")
        choice = input("Select Category: ")

        if choice == '4': break
        
        entity = {'1': 'College', '2': 'Program', '3': 'Student'}.get(choice)
        if not entity: continue
        
        while True:
            print(f"\n--- {entity.upper()} MENU ---")
            print("1. Add New")
            print("2. List All")
            print("3. Search")
            print("4. Update")
            print("5. Delete")
            print("6. Back")
            
            act = input("Action: ")
            if act == '6': break

            if act == '1':
                new_row = {f: input(f"Enter {f}: ") for f in sis.headers[entity]}
                sis.create(entity, new_row)
            
            elif act == '2':
                sort_f = input(f"Sort by {sis.headers[entity]} (Enter to skip): ")
                print_table(sis.list_all(entity, sort_by=sort_f), sis.headers[entity])
            
            elif act == '3':
                field = input(f"Field to search {sis.headers[entity]}: ")
                val = input("Search term: ")
                print_table(sis.search(entity, field, val), sis.headers[entity])
            
            elif act == '4':
                pk_val = input(f"Enter {sis.headers[entity][0]} to update: ")
                print("(Leave blank to keep existing value)")
                updates = {f: input(f"New {f}: ") for f in sis.headers[entity][1:]}
                sis.update(entity, pk_val, updates)
            
            elif act == '5':
                pk_val = input(f"Enter {sis.headers[entity][0]} to delete: ")
                # New Confirmation Logic
                confirm = input(f"Are you sure you want to delete {pk_val}? (y/n): ")
                if confirm.lower() == 'y':
                    sis.delete(entity, pk_val)
                else:
                    print("Deletion cancelled.")

if __name__ == "__main__":
    main_menu()