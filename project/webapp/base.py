from sched import scheduler
from ortools.sat.python import cp_model
from database.db_utils import fetch_all_employees, fetch_all_shifts, fetch_all_unavailable_days, fetch_all_shift_preferences, fetch_all_seniority, fetch_all_shift_requirements, fetch_shift_requirements_for_bartenders, fetch_shift_requirements_for_barbacks
import matplotlib.pyplot as plt
import numpy as np


class Scheduler:
    def __init__(self, role, employee_data=None, shift_data=None, preferences=None, seniority=None, shift_requirements=None):
        
        self.role = role
        self.employee_names = [name for name, emp_role in employee_data if emp_role == role]
        self.shift_names = [name for name, shift_role in shift_data if shift_role == role]
        self.unavailable_days = preferences['unavailable_days'] if preferences else {}# Dictionary to hold days an employee is unavailable. Key is employee index and value is list of days.
        self.shift_preferences = preferences['shift_preferences'] if preferences else {}# Dictionary to hold employee shift preferences. Key is employee index and value is another dictionary mapping day index to preference score.
        # Ensure all employees have a numeric seniority score
        default_seniority = 5  # Define a default seniority score
        self.seniority = {e: seniority.get(e, default_seniority) if isinstance(seniority.get(e), (int, float)) else default_seniority for e in range(len(self.employee_names))}

        # List of lists for shift requirements
        self.shift_requirements = shift_requirements if shift_requirements else []
    

    def generate_schedule(self):
        """Generates the optimal schedule based on provided data."""
        num_employees = len(self.employee_names)
        num_days = 7
        num_shifts = len(self.shift_names)
        all_employees = range(num_employees)
        all_days = range(num_days)
        all_shifts = range(num_shifts)

        model = cp_model.CpModel()

        # Create binary variables to determine if an employee 'e' is working on a shift 's' on day 'd'.
        shifts = {}
        for e in all_employees:
            for d in all_days:
                for s in all_shifts:
                    shifts[(e, d, s)] = model.NewBoolVar('shift_e%id%is%i' % (e, d, s))

        # Variables to hold penalties for not meeting soft constraints.
        penalties = {}
        for e in all_employees:
            penalties[e] = model.NewIntVar(0, num_days, 'penalty_e%i' % e)

        # Hard constraints

        # Each shift is assigned to exactly one employee
        for d in all_days:
            for s in all_shifts:
                model.Add(sum(shifts[(e, d, s)] for e in all_employees) == self.shift_requirements[d][s])

        # Adds unavailable days, with a check to prevent KeyError
        for e, days in self.unavailable_days.items():
            for d in days:
                if all((e, d, s) in shifts for s in all_shifts):
                    model.Add(sum(shifts[(e, d, s)] for s in all_shifts) == 0)
                else:
                    print(f"Skipping constraint for employee {e} on day {d} due to missing shift index.")                  

        # Each employee works at most one shift per day
        for e in all_employees:
            for d in all_days:
                model.Add(sum(shifts[(e, d, s)] for s in all_shifts) <= 1)

        # Each employee works at most five shifts per week
        for e in all_employees:
            total_shifts = sum(shifts[(e, d, s)] for d in all_days for s in all_shifts)
            model.Add(total_shifts <= 5)

        # Soft constraints

        # Each employee works at least two shifts per week
        for e in all_employees:
            total_shifts = sum(shifts[(e, d, s)] for d in all_days for s in all_shifts)
            # The penalty is the difference between 2 and the total number of shifts (if positive)
            model.Add(penalties[e] >= 2 - total_shifts)

        # Objective function

        # Preference score for the schedule
        default_preference = 1
        preference_score = sum(
            shifts[(e, d, s)] * self.shift_preferences.get(e, {}).get(d, default_preference)
            for e in all_employees for d in all_days for s in all_shifts
        )
        
        # Debugging statements
        for e in all_employees:
            print(f"Employee {e}, Seniority: {self.seniority[e]}, Type: {type(self.seniority[e])}")

        # Seniority score for the schedule
        seniority_score = sum(shifts[(e, d, s)] * self.seniority[e] for e in all_employees for d in all_days for s in all_shifts)

        # Penalty for not working at least two shifts per week
        total_penalty = sum(penalties[e] for e in all_employees)

        # The objective is to maximize the sum of the preference and seniority scores, minus the total penalty
        model.Maximize(preference_score + 2 * seniority_score - total_penalty)

        # Creates the solver and solve
        solver = cp_model.CpSolver()
        solver.Solve(model)

        # Build the schedule
        schedule = {}
        for d in all_days:
            schedule[d] = {}
            for s in all_shifts:
                schedule[d][s] = []
                for e in all_employees:
                    if solver.Value(shifts[(e, d, s)]) == 1:
                        schedule[d][s].append(self.employee_names[e])

        # Build total shifts for each employee
        total_shifts_per_employee = {}
        for e in all_employees:
            total_shifts = sum(solver.Value(shifts[(e, d, s)]) for d in all_days for s in all_shifts)
            total_shifts_per_employee[self.employee_names[e]] = total_shifts
        
        formatted_schedule = [
            {
                'day': day,
                'shifts': [
                    {'shift_name': self.shift_names[s], 'employees': schedule[day][s]}
                    for s in schedule[day]
                ]
            }
            for day in schedule
        ]

        # Convert total shifts per employee to a list of dictionaries
        formatted_total_shifts = [
            {'employee_name': emp, 'total_shifts': total_shifts_per_employee[emp]}
            for emp in total_shifts_per_employee
        ]
        
        return formatted_schedule, formatted_total_shifts
    

def get_input_data(role):
    # Employees' names
    employees = fetch_all_employees()
    employee_names = [(emp[1], emp[2]) for emp in employees if emp[2] == role]
    
    # Shift names
    shifts = fetch_all_shifts()
    shift_names = [(shift[1], shift[2]) for shift in shifts if shift[2] == role]
    
    unavailableDays = fetch_all_unavailable_days()
    unavailable_days = {} 
    for employee_id, day in unavailableDays:
        if employee_id not in unavailable_days:
            unavailable_days[employee_id] = []
        unavailable_days[employee_id].append(day)
        
    # Employees' shift preferences (higher is better): [morning, night, all_day]
    shiftPreferences = fetch_all_shift_preferences()
    shift_preferences = {}
    for employee_id, day, score in shiftPreferences:
        if employee_id not in shift_preferences:
            shift_preferences[employee_id] = {}
        shift_preferences[employee_id][day] = score
    
    # senority 
    fetch_senior = fetch_all_seniority()
    seniority = {}
    for employee_id, score in fetch_senior:
        seniority[employee_id] = score
        
    # Shift requirements data
    if role == 'bartender':
        all_shift_requirements = fetch_shift_requirements_for_bartenders()
    elif role == 'barback':
        all_shift_requirements = fetch_shift_requirements_for_barbacks()
    else:
        raise ValueError(f"Unsupported role: {role}")
    
    # Determine the range of shifts for the role
    shift_ids = [shift_id for _, shift_id, _ in all_shift_requirements]
    min_shift_id = min(shift_ids)
    max_shift_id = max(shift_ids)
        
    # Manager inputs number of employees needed for each shift on each day
    shift_requirements = []
    for day in range(7):
        daily_requirements = []
        for shift in range(min_shift_id, max_shift_id + 1):
            req = next((x[2] for x in all_shift_requirements if x[0] == day and x[1] == shift), 0)
            daily_requirements.append(req)
        shift_requirements.append(daily_requirements)
    
    return employee_names, shift_names, {'unavailable_days': unavailable_days, 'shift_preferences': shift_preferences}, seniority, shift_requirements


def main():
    # Schedule for bartenders
    bartender_data = get_input_data('bartender')
    bartender_scheduler = Scheduler('bartender', *bartender_data)
    bartender_schedule, bartender_shifts_per_employee = bartender_scheduler.generate_schedule()


    # Schedule for barbacks
    barback_data = get_input_data('barback')
    barback_scheduler = Scheduler('barback', *barback_data)
    barback_schedule, barback_shifts_per_employee = barback_scheduler.generate_schedule()

    
    bartender_schedule, _ = bartender_scheduler.generate_schedule()
    #print_schedule('Bartender', bartender_schedule, bartender_shifts_per_employee)
    
    barback_schedule, _ = barback_scheduler.generate_schedule()
    print_schedule('Barback', barback_schedule, barback_shifts_per_employee)
    

def print_schedule(role, schedule, formatted_total_shifts):
    print(f"\nSchedule for {role}:\n")
    for day_info in schedule:
        print(f"Day {day_info['day'] + 1}:")  # Assuming 'day' is 0-indexed
        for shift_info in day_info['shifts']:
            if shift_info['employees']:
                employees = ', '.join(shift_info['employees'])
                print(f"  {shift_info['shift_name']}: {employees}")
            else:
                print(f"  {shift_info['shift_name']}: No employees assigned")
        print()  # Newline for readability

    # Printing total shifts per employee
    print(f"Total Shifts per Employee for {role}:\n")
    for employee_info in formatted_total_shifts:
        employee = employee_info['employee_name']
        total_shifts = employee_info['total_shifts']
        print(f"{employee}: {total_shifts} shifts")
    print()  # Newline for readability
    



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred while setting up the schedule: {e}")