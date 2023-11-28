from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session  # If you are using server-side sessions

from blueprints.employees_blueprint import employees
from blueprints.shifts_blueprint import shifts
from blueprints.create_schedule_blueprint import create_schedule
from blueprints.output_blueprint import output
from blueprints.auth_blueprint import auth

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # This should be a random byte string.

app.register_blueprint(employees, url_prefix='/employees')
app.register_blueprint(shifts, url_prefix='/shifts')
app.register_blueprint(create_schedule, url_prefix='/create_schedule')
app.register_blueprint(output, url_prefix='/output')
app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def view():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(threaded=False)
