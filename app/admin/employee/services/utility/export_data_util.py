
from fastapi import HTTPException
from io import BytesIO
import json
from bson import json_util
from pdfkit.configuration import Configuration
import pdfkit


def export_data(data, export_format):
    if export_format == "csv":
        output = BytesIO()
        data.to_csv(output, index=False)
        csv_data = output.getvalue()
        return csv_data, "text/csv"
    elif export_format == "xlsx":
        output = BytesIO()
        data.to_excel(output, index=False)
        xlsx_data = output.getvalue()
        return xlsx_data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif export_format == "pdf":
        # Provide the path to wkhtmltopdf executable
        # Provide the correct path to wkhtmltopdf executable
        config = Configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
                
        pdf_data = pdfkit.from_string(data.to_html(index=False), False, configuration=config)
        return pdf_data, "application/pdf"
    else:
        raise HTTPException(status_code=400, detail="Invalid export format")


def get_salary_data(data):
    return {
        "ctc_template": data.get("ctc_template"),
        "annual_ctc": data.get("annual_ctc"),
        "earning": {
            "monthly_ctc": data.get("earning", {}).get("monthly_ctc"),
            "basic": data.get("earning", {}).get("basic"),
            "da": data.get("earning", {}).get("da"),
            "hra": data.get("earning", {}).get("hra"),
            "allowances": data.get("earning", {}).get("allowances"),
            "other_special_allowances": data.get("earning", {}).get("other_special_allowances"),
        },
        "deduction": {
            "epf": data.get("deduction", {}).get("epf"),
            "esic": data.get("deduction", {}).get("esic"),
            "pt": data.get("deduction", {}).get("pt"),
            "gratuity": data.get("deduction", {}).get("gratuity"),
            "medical_insurance": data.get("deduction", {}).get("medical_insurance"),
            "others": data.get("deduction", {}).get("others"),
        },
        "gross_salary": data.get("gross_salary"),
        "net_salary": data.get("net_salary"),
        "employee_id": data.get("employee_id"),
    }

# Define the get_bank_data function
def get_bank_data(data):
    return {
        "bank_name": data.get("bank_name"),
        "ifsc_code": data.get("ifsc_code"),
        "account_number": data.get("account_number"),
        "branch_code": data.get("branch_code"),
    }




class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return json_util.default(obj)
    

# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         return json_util.default(obj)

# json_encoder = CustomJSONEncoder()