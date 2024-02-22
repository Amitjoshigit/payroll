
from fastapi import HTTPException
import json
from fastapi.encoders import jsonable_encoder

from app.admin.employee.schema.ctc_breakup_schema import EmployeeInput
from app.admin.DB_connection import employee_salaries_collection, employee_basic_collection


def allowance(row, config):
    for grades in config['allowance']:
        if grades['grade'] == row:
            return [grades['food_allowance'], grades['conveyance_allowance'], grades['medical_allowance'],
                    grades['internet_allowance']]


def special_allowance(expected_ctc, basic, hra, allowance, company_pf, config, learning_rate=0.015, max_iterations=1000,
                      tolerance=0.0):
    # Check if expected CTC is too low
    if expected_ctc <= 10000:
        return 0, 0

    # Initialize special allowance
    sp = 1000

    # Calculate gross salary
    gross = basic + hra + allowance + sp

    iteration = 0
    while True:
        # Calculate ESIC based on condition and percentage from config
        esic_condition = config['Formula_inputs']['ESIC']['company']['condition']
        esic_percentage = eval(config['Formula_inputs']['ESIC']['company']['percentage'])
        if eval(esic_condition):
            esic = gross * esic_percentage
        else:
            esic = config['Formula_inputs']['ESIC']['company']['else']

        # Calculate CTC and error
        gross = basic + hra + allowance + sp
        ctc = gross + company_pf + esic
        error = ctc - expected_ctc

        # Check if the error is within the tolerance level
        if error == tolerance:
            break

        # Update special allowance using gradient descent
        sp -= learning_rate * error

        iteration += 1
        if iteration >= max_iterations:
            break
    return sp, esic, error, gross


def save_to_employee_salaries_collection(employee_id, result, employee: EmployeeInput):

    # Include annual_ctc and ctc_template in the result
    result["annual_ctc"] = employee.annual_ctc
    result["ctc_template"] = employee.ctc_template

    # Remove the ObjectId and insert the employee_id
    result.pop("_id", None)
    result["employee_id"] = employee_id

    # Use jsonable encoder to encode the result as JSON
    result = jsonable_encoder(result)
    # Insert or update the result in the "employee_salaries" collection
    employee_salaries_collection.update_one(
        {"employee_id": employee_id},
        {"$set": result},
        upsert=True  # This will insert a new document if it doesn't exist
    )


def calculate_ctc(employee: EmployeeInput):
    try:
        # Fetch employee details from MongoDB based on the provided 'employee_id'
        employee_data_from_db = employee_basic_collection.find_one({"employee_id": employee.employee_id})

        if not employee_data_from_db:
            raise HTTPException(status_code=404, detail=f"Employee with ID {employee.employee_id} not found")

        # Read the configuration from file
        with open("app/admin/employee/services/utility/ctc_api.json", "r") as config_file:
            config = json.load(config_file)

        # Considering grade as g4.0 by default
        grade = 'g4.0'

        monthly_ctc = employee.annual_ctc / 12
        # Calculate basic, hra, and comp_epf using the provided formulas in the configuration
        basic = monthly_ctc * config["Formula_inputs"]["basic"]
        hra = basic * config["Formula_inputs"]["hra"]
        comp_epf = basic * config["Formula_inputs"]["company_contribution"]["epf"]

        # Perform calculations using the provided Python code (Template A)
        food_allowance, conveyance_allowance, medical_allowance, internet_allowance = allowance(grade, config)

        special_allowance_value, comp_esic, error, gross = special_allowance(
            monthly_ctc,
            basic,
            hra,
            food_allowance + conveyance_allowance + medical_allowance + internet_allowance,
            comp_epf,
            config
        )

        # Assuming that emp_epf is the employee's contribution to EPF
        emp_epf = basic * config['Formula_inputs']['employee_Deductions']['epf'] if basic <= 15000 else 1800

        # Assuming that emp_esic is the employee's contribution to ESIC
        emp_esic = basic * config['Formula_inputs']['employee_Deductions']['esi'] if gross <= 21000 else 0

        # Assuming that PT is Professional Tax
        PT = config['Formula_inputs']['PT']['amount'] if eval(config['Formula_inputs']['PT']['condition'],
                                                              None, {'gross': gross}) else 0

        # Assuming that total_deductions is the sum of employee and company contribution to EPF and ESIC
        total_deductions = emp_epf + emp_esic

        # Assuming that net_salary is the gross salary minus total_deductions
        net_salary = gross - emp_epf - emp_esic - PT

        # Calculate the sum of allowances
        allowances_sum = sum([food_allowance, conveyance_allowance, medical_allowance, internet_allowance])

        # Create a dictionary containing the calculated values
        result = {
            "earning": {
                "monthly_ctc": monthly_ctc,
                "basic": basic,
                "da": 0,
                "hra": hra,
                "allowances": allowances_sum,

                "other_special_allowance": special_allowance_value,

            },
            "deduction": {
                "epf": emp_epf,
                "esic": emp_esic,
                "pt": PT,
                "gratuity": 0,
                "medical_insurance": 0,
                "others": 0,
            },
            "net_salary": net_salary,
            "gross_salary": gross
        }

        # Save the result to the employee_salaries_collection
        save_to_employee_salaries_collection(employee.employee_id, result, employee)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

