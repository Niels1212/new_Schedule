import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for
import database.db_utils as db_utils
from database.insert_data import SchedulingDB

employees = Blueprint('employees', __name__)
scheduling_db = SchedulingDB('scheduling.db')
day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}


@employees.route('/view')
def view():
    data = db_utils.fetch_all_employees()
    return render_template('employees/employee_view.html', data=data)

@employees.route('/add', methods=['GET'])
def add_employee_form():
    # This route only handles the GET request to display the form
    return render_template('employees/employee_add.html')

@employees.route('/add', methods=['POST'])
def add_employee():
    # Get the form data
    employee_name = request.form['employee_name']
    employee_role = request.form['employee_role'] 
    print("Adding employee:", employee_name, "Role:", employee_role)
    # Insert into the database (using your custom function)
    scheduling_db = SchedulingDB('scheduling.db')
    # Insert into the database
    try:
        scheduling_db.insert_employee(employee_name, employee_role)
        return redirect(url_for('employees.view'))
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")
        return "Error adding employee", 500

@employees.route('/edit/<int:employee_id>', methods=['GET'])
def edit_employee_form(employee_id):
    # Fetch the current data of the employee
    employee_data = db_utils.fetch_employee_by_id(employee_id)
    if employee_data:
        return render_template('employees/employee_edit.html', employee=employee_data)
    else:
        return "Employee not found", 404

@employees.route('/edit/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    # Get the form data
    new_name = request.form['employee_name']
    new_role = request.form['employee_role']
    # Update in the database (using your custom function)
    scheduling_db = SchedulingDB('scheduling.db')
    try:
        scheduling_db.update_employee(employee_id, new_name, new_role)
        return redirect(url_for('employees.view'))
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")
        return "Error updating employee", 500

@employees.route('/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    try:
        scheduling_db.delete_employee(employee_id)
        return redirect(url_for('employees.view'))
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error deleting employee", 500
    
@employees.route('/details/<int:employee_id>')
def employee_details(employee_id):
    employee = db_utils.fetch_employee_by_id(employee_id)
    if not employee:
        return "Employee not found", 404
    
    # Fetch additional details
    availability = [(employee_id, day_names[day]) for employee_id, day in db_utils.fetch_all_unavailable_days_for_employee(employee_id)]
    raw_preferences = db_utils.fetch_all_shift_preferences_for_employee(employee_id)
    preferences = [(day_names.get(pref[1], "Unknown Day"), pref[2]) for pref in raw_preferences if pref[1] in day_names]
    employee_seniority = db_utils.fetch_seniority_for_employee(employee_id)
    
    # Render the details template
    return render_template('employees/employee_details.html', 
                           employee=employee,
                           availability=availability, 
                           preferences=preferences, 
                           seniority=employee_seniority)
    

@employees.route('/edit_details/<int:employee_id>')
def edit_employee_details(employee_id):
    employee = db_utils.fetch_employee_by_id(employee_id)
    availability = db_utils.fetch_all_unavailable_days_for_employee(employee_id)
    raw_preferences = db_utils.fetch_all_shift_preferences_for_employee(employee_id)

    # Convert preferences to a dictionary
    preferences = {pref[1]: pref[2] for pref in raw_preferences}

    seniority = db_utils.fetch_seniority_for_employee(employee_id)

    return render_template('employees/employee_details_edit.html', 
                           employee=employee,
                           availability=availability,
                           preferences=preferences,
                           seniority=seniority,
                           day_names=day_names)
    
@employees.route('/update_unavailable_days/<int:employee_id>', methods=['POST'])
def update_unavailable_days(employee_id):
    # Get the list of checked days from the form
    checked_days = request.form.getlist('unavailable_days')
    checked_days = [int(day) for day in checked_days]  # Convert days to integers
    print("Checked Days:", checked_days) 

    # Update the database
    try:
        scheduling_db.delete_unavailable_days(employee_id)  # Clear existing records
        scheduling_db.insert_unavailable_days(employee_id, checked_days)  # Add new records
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle your error or flash a message to the user
    return redirect(url_for('employees.employee_details', employee_id=employee_id))


@employees.route('/update_shift_preferences/<int:employee_id>', methods=['POST'])
def update_shift_preferences(employee_id):
    # Get the new preferences from the form
    new_preferences = {}
    for day in range(0, 7):  # Assuming days 1-7 for Monday-Sunday
        preference = request.form.get(f'preference_{day}', 0)
        new_preferences[day] = int(preference)  # Convert to integer

    # Update the database
    try:
        # Clear existing preference records
        scheduling_db.delete_shift_preferences(employee_id)

        # Insert new preference records
        for day, pref in new_preferences.items():
            scheduling_db.insert_shift_preference(employee_id, day, pref)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle your error or flash a message to the user
    
    return redirect(url_for('employees.employee_details', employee_id=employee_id))


@employees.route('/update_seniority/<int:employee_id>', methods=['POST'])
def update_seniority(employee_id):
    new_seniority = request.form.get('seniority', 0)
    try:
        scheduling_db.update_seniority(employee_id, new_seniority)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle your error or flash a message to the user
    return redirect(url_for('employees.employee_details', employee_id=employee_id))
