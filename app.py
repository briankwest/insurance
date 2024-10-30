from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from urllib.parse import urlsplit, urlunsplit
from dotenv import load_dotenv
import os

load_dotenv()

HTTP_USERNAME = os.getenv('HTTP_USERNAME')
HTTP_PASSWORD = os.getenv('HTTP_PASSWORD')

app = Flask(__name__)
auth = HTTPBasicAuth()

SWAIG_FUNCTION_SIGNATURES = {
    "verify_insurance": {
        "description": "Verify the insurance provider and confirm active status",
        "function": "verify_insurance",
        "parameters": {
            "type": "object",
            "properties": {
                "insurance_provider": {"type": "string", "description": "The user's insurance provider name."},
                "member_id": {"type": "string", "description": "The insurance member ID number."},
                "date_of_birth": {"type": "string", "description": "The user's date of birth in YYYY-MM-DD format."}
            },
            "required": ["insurance_provider", "member_id", "date_of_birth"]
        }
    },
    "check_eligibility": {
        "description": "Check coverage for online therapy under the insurance plan",
        "function": "check_eligibility",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "The insurance member ID number."}
            },
            "required": ["member_id"]
        }
    },
    "schedule_therapy_session": {
        "description": "Schedule a therapy session for the user with an eligible therapist",
        "function": "schedule_therapy_session",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "The insurance member ID number for scheduling."},
                "preferred_date": {"type": "string", "description": "The preferred date for the therapy session in YYYY-MM-DD format."},
                "preferred_time": {"type": "string", "description": "The preferred time for the therapy session in minitary time format (HH:MM)."},
                "therapist_id": {"type": "string", "description": "The ID of the therapist for the session."}
            },
            "required": ["member_id", "preferred_date", "preferred_time", "therapist_id"]
        }
    },
    "get_therapist_info": {
        "description": "Retrieve therapists available within the user's insurance network",
        "function": "get_therapist_info",
        "parameters": {
            "type": "object",
            "properties": {
                "insurance_provider": {"type": "string", "description": "The insurance provider accepted by the therapist."}
            },
            "required": ["insurance_provider"]
        }
    },
    "provide_copay_information": {
        "description": "Retrieve copayment amount for therapy sessions",
        "function": "provide_copay_information",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "The insurance member ID number."}
            },
            "required": ["member_id"]
        }
    }
}

@app.route('/swaig', methods=['POST'])
@auth.verify_password
def swaig_handler():
    data = request.json

    action = data.get('action')

    if action == "get_signature":
        requested_functions = data.get("functions")
        print(f"Requested functions: {requested_functions}")

        if not requested_functions:
            requested_functions = list(SWAIG_FUNCTION_SIGNATURES.keys())
        
        host_url = request.host_url.rstrip('/')

        for func in SWAIG_FUNCTION_SIGNATURES:
            split_url = urlsplit(host_url)

            if HTTP_USERNAME and HTTP_PASSWORD:
                netloc = f"{HTTP_USERNAME}:{HTTP_PASSWORD}@{split_url.netloc}"
            else:
                netloc = split_url.netloc
            if split_url.scheme != 'https':
                split_url = split_url._replace(scheme='https')

            new_url = urlunsplit((split_url.scheme, netloc, split_url.path, split_url.query, split_url.fragment))
            SWAIG_FUNCTION_SIGNATURES[func]["web_hook_url"] = f"{new_url}/swaig"
        
        if requested_functions == '':
            requested_functions = avaliable_functions

        response = [
            SWAIG_FUNCTION_SIGNATURES[func] 
            for func in requested_functions 
            if func in SWAIG_FUNCTION_SIGNATURES
        ]

        missing_functions = [
            func for func in requested_functions 
            if func not in SWAIG_FUNCTION_SIGNATURES
        ]

        print(f"missing_functions: {missing_functions}")

        return jsonify(response) 

    else:
        function_name = data.get('function')
        argument = data.get('argument', {})
        params = argument.get('parsed', [{}])[0]
        print(f"Function name: {function_name}, Params: {params}")

        function_map = {
            func_name: globals()[func_name] 
            for func_name in SWAIG_FUNCTION_SIGNATURES.keys() 
            if func_name in globals()
        }

        if function_name in function_map:
            response = function_map[function_name](**params)
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Function not found"}), 404

def verify_insurance(member_id=None, insurance_provider=None, date_of_birth=None):
    data = request.json
    human_readable_mock_data = "Member ID: 123456789, Provider: Blue Cross Blue Shield, Date of Birth: 1980-01-01, Status: active"
    return human_readable_mock_data

def check_eligibility(member_id=None):
    data = request.json
    eligibility_data = {
        "123456789": ["online_therapy", "in_person_therapy"]
    }
    member_id = data["argument"]["parsed"][0]["member_id"]

    if member_id in eligibility_data:
        covered_services = ', '.join(eligibility_data[member_id])
        return f"Success: The member is covered for the following services: {covered_services}."
    return "Error: No coverage for online therapy."

def schedule_therapy_session(member_id=None, preferred_date=None, preferred_time=None, therapist_id=None):
    return f"Success: Session scheduled on {preferred_date} at {preferred_time} with therapist {therapist_id}."

def get_therapist_info(insurance_provider=None):
    therapists = [
        {"id": "therapist_1", "name": "Dr. Smith", "specialty": "Cognitive Behavioral Therapy"},
        {"id": "therapist_2", "name": "Dr. Jones", "specialty": "Family Therapy"}
    ]
    human_readable_data = "Available therapists: " + ", ".join(
        [f"{therapist['name']} specializes in {therapist['specialty']}" for therapist in therapists]
    )
    return human_readable_data

def provide_copay_information(member_id=None):
    data = request.json
    copay_info = {
        "123456789": {"copay": 20}
    }
    if member_id in copay_info:
        return f"Member ID {member_id} has a copay of ${copay_info[member_id]['copay']}."
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)