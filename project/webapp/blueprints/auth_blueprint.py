# blueprints/auth_blueprint.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import database.db_utils as db_utils
from database.insert_data import SchedulingDB

auth = Blueprint('auth', __name__, template_folder='templates')

db = SchedulingDB('scheduling.db')  # Initialize your database access

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'employee'  # Or you could have this as a field in your form

        hashed_password = generate_password_hash(password)
        
        try:
            db.insert_user(username, hashed_password, role)
            flash('Registration successful!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Registration failed. User may already exist.')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db_utils.fetch_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login successful!')
            return redirect(url_for('view'))  # Modify as necessary
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

# Make sure to import and register the blueprint in your app.py
