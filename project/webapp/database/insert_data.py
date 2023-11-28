import sqlite3


# Employees' names
employee_names =  ["Dani Bricelo", "Ramon Ombrellino", "Robert Ima", 
                  "Jonathan Politz", "Lizbeth Santana", "Adelaide Albuquerque", 
                  "Francisco Moreno", "Christal Ankins", "Camila Rodriguez", 
                  "Stephanie Jonson", "Ty Miller", "Rocio Salto", "Melissa Doyle", 
                  "Larry Obregon", "facuendo farias","pepe salgado", "pepe ongito"]

# Shift names
shift_names = ["Main Bar Opener", "Courtyard Opener", 
               "Swing Inside", "Swing Outside", 
               "Main Bar Closer", "Courtyard Closer", 
               "Southwing Opener", "Southwing Closer", "Event"]

unavailable_days = {1:[1,2,3,4,5,6], 5:[1,3], 9:[4]}  # Employees input days they can't work

# Employees' shift preferences (higher is better): [morning, night, all_day]
shift_preferences = {
        0: {},  
        2: {}, 
        3: {}, 
        4: {}, 
        5: {}, 
        6: {},
        7: {}, 
        8: {},  
        9: {4: 10}, #Empleado 9 tiene 10/10 ganas de trabajr dia 4
        10: {6:5}, #Empleado 10 tiene 5/10 ganas de trabajar dia 6
        11: {}, 
        12: {4: 10, 5: 10, 6:10}, 
        13: {}, 
        14: {},
        15:{}
        }
# senority 
seniority = {
    0: 10, 1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 
    8: 10, 9: 10, 10: 10, 11: 10, 12: 10, 13: 10, 14: 10, 15: 10, 16: 10, 17: 10
}   
# Manager inputs number of employees needed for each shift on each day
shift_requirements = [
            #main bar, Courtyard Opener, Swing Inside, Swing Outside, Main Bar Closer, Courtyard Closer, Southwing Opener, Southwing Closer, Event
            [1, 1, 1, 1, 1, 1, 1, 1, 0],  # Monday
            [1, 1, 1, 0, 1, 2, 1, 1, 1],  # Tuesday
            [1, 1, 0, 1, 1, 1, 1, 1, 0],  # Wednesday
            [1, 1, 1, 1, 1, 1, 1, 1, 0],  # Thursday
            [1, 1, 1, 0, 1, 1, 1, 2, 2],  # Friday
            [1, 1, 1, 1, 1, 1, 1, 1, 5],  # Saturday
            [0, 0, 0, 0, 0, 0, 1, 1, 1]   # Sunday
        ]

class SchedulingDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
    def insert_user(self, username, hashed_password, role):
        """Insert a new user into the Users table."""
        self.cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                            (username, hashed_password, role))
        self.conn.commit()

    # Employee Data
    def insert_employee(self, name, role):
        self.cursor.execute("INSERT INTO Employees (name, role) VALUES (?, ?)", (name, role))
        self.conn.commit()
    def update_employee(self, employee_id, new_name, new_role):
        self.cursor.execute("UPDATE Employees SET name = ?, role = ? WHERE id = ?", (new_name, new_role, employee_id))
        self.conn.commit()
    def delete_employee(self, employee_id):
        self.cursor.execute("DELETE FROM Employees WHERE id = ?", (employee_id,))
        self.conn.commit()

    # Shift Data
    def insert_shift(self, name, role_type):
        self.cursor.execute("INSERT INTO Shifts (name, role_type) VALUES (?, ?)", (name, role_type))
        self.conn.commit()
    def update_shift_name(self, shift_id, new_name, new_role_type):
        self.cursor.execute("UPDATE Shifts SET name = ?, role_type = ? WHERE id = ?", (new_name, new_role_type, shift_id))
        self.conn.commit()
    def delete_shift(self, shift_id):    
        self.cursor.execute("DELETE FROM Shifts WHERE id = ?", (shift_id,))
        self.conn.commit()
    
    # Unavailable Days Data
    def insert_unavailable_days(self, employee_id, days):
        for day in days:
                self.cursor.execute("INSERT INTO UnavailableDays (employee_id, day) VALUES (?, ?)", (employee_id, day))
        self.conn.commit()
    def delete_unavailable_days(self, employee_id):
        self.cursor.execute("DELETE FROM UnavailableDays WHERE employee_id = ?", (employee_id,))
        self.conn.commit()
    
    # Shift Preferences Data
    def insert_shift_preference(self, employee_id, day, preference):
        self.cursor.execute("INSERT INTO ShiftPreferences (employee_id, day, preference) VALUES (?, ?, ?)", (employee_id, day, preference))
        self.conn.commit()
    def update_shift_preference(self, employee_id, day, new_preference):
        self.cursor.execute("UPDATE ShiftPreferences SET preference = ? WHERE employee_id = ? AND day = ?", (new_preference, employee_id, day))
        self.conn.commit()
    def delete_shift_preference(self, employee_id, day):
        self.cursor.execute("DELETE FROM ShiftPreferences WHERE employee_id = ? AND day = ?", (employee_id, day))
        self.conn.commit()
    
    # Seniority Data
    def insert_seniority(self, employee_id, score):
        self.cursor.execute("INSERT INTO Seniority (employee_id, score) VALUES (?, ?)", (employee_id, score))
        self.conn.commit()
    def update_seniority(self, employee_id, new_score):
        self.cursor.execute("UPDATE Seniority SET score = ? WHERE employee_id = ?", (new_score, employee_id))
        self.conn.commit()
    def delete_seniority(self, employee_id):
        self.cursor.execute("DELETE FROM Seniority WHERE employee_id = ?", (employee_id,))
        self.conn.commit()
    
    # Shift Requirements Data
    def update_shift_requirement(self, day, shift_id, new_required_employees):
        self.cursor.execute("UPDATE ShiftRequirements SET required_employees = ? WHERE day = ? AND shift_id = ?", (new_required_employees, day, shift_id))
        self.conn.commit()
    
    def delete_shift_preferences(self, employee_id):
        self.cursor.execute("DELETE FROM ShiftPreferences WHERE employee_id = ?", (employee_id,))
        self.conn.commit()
        
    def close(self):
        self.conn.close()
    
def main():
    db = SchedulingDB('scheduling.db')

    # Sample operations
    db.close()

if __name__ == "__main__":
    main()    
    print("Done")

