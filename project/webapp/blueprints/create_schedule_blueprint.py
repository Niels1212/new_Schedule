import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for, flash
import database.db_utils as db_utils
from database.insert_data import SchedulingDB

create_schedule = Blueprint('create_schedule', __name__)
scheduling_db = SchedulingDB('scheduling.db')

@create_schedule.route('/view')
def view():
    return render_template('create_schedule/create_schedule_landing.html')

@create_schedule.route('/create_schedule/bartender', methods=['GET', 'POST'])
def manage_create_schedule_bartender():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_with_indices = list(enumerate(days))

    if request.method == 'POST':
        # Update shift requirements based on the form data
        for day_idx, _ in days_with_indices:
            for shift_idx in range(9):  # Assuming bartenders have shifts 0 to 8
                input_name = f"requirement_{day_idx}_{shift_idx}"
                new_requirement = request.form.get(input_name)
                if new_requirement is not None:
                    scheduling_db.update_shift_requirement(day_idx, shift_idx, int(new_requirement))
        flash("Schedule Updated")  # Flash the message

    # Fetch shift requirements for bartenders
    all_bartender_shift_requirements = db_utils.fetch_shift_requirements_for_bartenders()
    shift_requirements = [[0] * 9 for _ in range(7)]  # Initialize for 7 days, 9 shifts
    for day, shift, count in all_bartender_shift_requirements:
        shift_requirements[day][shift] = count  # Adjust index if needed
    shift_names = ["Main Bar Opener", "Courtyard Opener", "Swing Inside", "Swing Outside", "Main Bar Closer", "Courtyard Closer", "Southwing Opener", "Southwing Closer", "Event" ]
    return render_template('create_schedule/create_schedule_bartenders.html', 
                           shift_requirements=shift_requirements, 
                           days=days_with_indices, 
                           role='Bartender',
                           shift_names=shift_names)
                          
@create_schedule.route('/create_schedule/barback', methods=['GET', 'POST'])
def manage_create_schedule_barback():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_with_indices = list(enumerate(days))

    if request.method == 'POST':
        # Update shift requirements based on the form data
        for day_idx, _ in days_with_indices:
            # Adjust range if the number of shifts for barbacks is different
            for shift_idx in range(9, 16):  # Assuming barbacks have shifts 9 to 15
                input_name = f"requirement_{day_idx}_{shift_idx}"
                new_requirement = request.form.get(input_name)
                if new_requirement is not None:
                    scheduling_db.update_shift_requirement(day_idx, shift_idx, int(new_requirement))
        flash("Barback Schedule Updated")  # Flash the message

    # Fetch shift requirements for barbacks
    print("Updated shift requirements:")
    all_barback_shift_requirements = db_utils.fetch_shift_requirements_for_barbacks()
    shift_requirements = [[0] * 7 for _ in range(7)]  # Initialize for 7 days, 7 shifts (adjust as needed)
    for day, shift, count in all_barback_shift_requirements:
        shift_requirements[day][shift - 9] = count  # Adjust the index based on shift range for barbacks

    # Define the shift names for barbacks
    shift_names = ["Main Bar Opener", "Courtyard Opener", "Southwing Opener", "Main Bar Closer", "Courtyard Closer", "Southwing Closer", "Event"]
    
    return render_template('create_schedule/create_schedule_barbacks.html', 
                           shift_requirements=shift_requirements, 
                           days=days_with_indices, 
                           role='Barback',
                           shift_names=shift_names)

