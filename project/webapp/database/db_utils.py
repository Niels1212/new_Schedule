import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'scheduling.db')

def create_connection():
    """Create a database connection and return the connection object."""
    connection = sqlite3.connect('C:\\Users\\niels\\OneDrive\\Desktop\\project\\scheduling.db')
    connection.row_factory = sqlite3.Row  # This line makes the rows returned act like dictionaries
    return connection

def fetch_user_by_username(username):
    """Fetch a user by their username."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def fetch_all_employees():
    """Fetch all employees from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

def fetch_employee_by_id(employee_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    employee = cursor.fetchone()
    conn.close()

    return employee

def fetch_employee_by_role(role):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE role = ?", (role,))
    employee = cursor.fetchall()
    conn.close()

    return employee

def fetch_all_employees_by_role(role):
    """Fetch all employees of a specific role from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees WHERE role = ?", (role,))
    employees = cursor.fetchall()
    conn.close()
    return employees

def fetch_all_shifts():
    """Fetch all shifts from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shifts")
    shifts = cursor.fetchall()
    conn.close()
    return shifts

def fetch_shifts_by_id(shift_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shifts WHERE id = ?", (shift_id,))
    shifts = cursor.fetchone()
    conn.close()
    return shifts


def fetch_all_unavailable_days():
    """Fetch all unavailable days from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unavailabledays")
    unavailable_days = cursor.fetchall()
    conn.close()
    return unavailable_days

def fetch_all_shift_preferences():
    """Fetch all shift preferences from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shiftpreferences")
    shift_preferences = cursor.fetchall()
    conn.close()
    return shift_preferences

def fetch_all_seniority():
    """Fetch all seniority scores from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seniority")
    seniority = cursor.fetchall()
    conn.close()
    return seniority

def fetch_all_shift_requirements():
    """Fetch all shift requirements from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shiftrequirements")
    shift_requirements = cursor.fetchall()
    conn.close()
    return shift_requirements

def fetch_shift_requirements_for_bartenders():
    """Fetch shift requirements for bartenders from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day, shift_id, required_employees FROM shiftrequirements WHERE role = 'bartender'")
    shift_requirements = cursor.fetchall()
    conn.close()
    return shift_requirements

def fetch_shift_requirements_for_barbacks():
    """Fetch shift requirements for barbacks from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day, shift_id, required_employees FROM shiftrequirements WHERE role = 'barback'")
    shift_requirements = cursor.fetchall()
    conn.close()
    return shift_requirements

def fetch_all_unavailable_days_for_employee(employee_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UnavailableDays WHERE employee_id = ?", (employee_id,))
    unavailable_days = cursor.fetchall()
    conn.close()
    return unavailable_days

def fetch_all_shift_preferences_for_employee(employee_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ShiftPreferences WHERE employee_id = ?", (employee_id,))
    preferences = cursor.fetchall()
    conn.close()
    return preferences

def fetch_seniority_for_employee(employee_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Seniority WHERE employee_id = ?", (employee_id,))
    seniority = cursor.fetchone()
    conn.close()
    return seniority

def fetch_shift_preference(employee_id, day):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ShiftPreferences WHERE employee_id = ? AND day = ?", (employee_id, day))
    cursor.fetchone()
    conn.close()
    return 

print(fetch_user_by_username('niels12'))
