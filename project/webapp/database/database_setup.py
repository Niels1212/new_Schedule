import sqlite3

def setup_database():
    # Connect to the SQLite database. If 'scheduling.db' doesn't exist, it'll create one.
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()

    # Create the Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    # Create the Shifts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Shifts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    # Create the UnavailableDays table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UnavailableDays (
            employee_id INTEGER,
            day INTEGER,
            FOREIGN KEY (employee_id) REFERENCES Employees(id)
        )
    """)
    
    # Create the ShiftPreferences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ShiftPreferences (
            employee_id INTEGER,
            day INTEGER,
            preference INTEGER,
            FOREIGN KEY (employee_id) REFERENCES Employees(id)
        )
    """)
    
    # Create the Seniority table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Seniority (
            employee_id INTEGER,
            score INTEGER,
            FOREIGN KEY (employee_id) REFERENCES Employees(id)
        )
    """)

    # Create the ShiftRequirements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ShiftRequirements (
            day INTEGER,
            shift_id INTEGER,
            required_employees INTEGER,
            FOREIGN KEY (shift_id) REFERENCES Shifts(id)
        )
    """)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Run the setup to create the database and tables
if __name__ == "__main__":
    setup_database()