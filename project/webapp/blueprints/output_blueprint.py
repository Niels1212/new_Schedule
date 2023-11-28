import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for, flash
import database.db_utils as db_utils
from database.insert_data import SchedulingDB
from base import Scheduler, get_input_data

output = Blueprint('output', __name__)

@output.route('/output/bartender')
def show_schedule_bartender():
    bartender_data = get_input_data('bartender')
    bartender_scheduler = Scheduler('bartender', *bartender_data)
    bartender_schedule, bartender_shifts_per_employee = bartender_scheduler.generate_schedule()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    all_bartenders = db_utils.fetch_employee_by_role('bartender')
    return render_template('schedule_bartenders.html', 
                           schedule=bartender_schedule, 
                           total_shifts=bartender_shifts_per_employee,
                           days_of_week=days_of_week,
                           all_bartenders=all_bartenders)
    
@output.route('/output/barback')
def show_schedule_barback():
    barback_data = get_input_data('barback')
    barback_scheduler = Scheduler('barback', *barback_data)
    barback_schedule, barback_shifts_per_employee = barback_scheduler.generate_schedule()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    all_barbacks = db_utils.fetch_employee_by_role('barback')
    return render_template('schedule_barbacks.html', 
                           schedule=barback_schedule, 
                           total_shifts=barback_shifts_per_employee,
                           days_of_week=days_of_week,
                           all_barbacks=all_barbacks)