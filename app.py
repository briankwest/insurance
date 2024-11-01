from flask import Flask
from dotenv import load_dotenv
import os
from signalwire_swaig.core import SWAIG, Parameter

load_dotenv()

# Initialize Flask and SWAIG
app = Flask(__name__)
swaig = SWAIG(
    app,
    auth=(os.getenv('HTTP_USERNAME'), os.getenv('HTTP_PASSWORD'))
)

# Mock data for examples
MOCK_DATA = {
    'insurance': {
        '123456789': {
            'provider': 'Blue Cross Blue Shield',
            'status': 'active',
            'copay': 20,
            'services': ['online_therapy', 'in_person_therapy']
        }
    },
    'therapists': [
        {"id": "t1", "name": "Dr. Smith", "specialty": "CBT"},
        {"id": "t2", "name": "Dr. Jones", "specialty": "Family Therapy"}
    ]
}

@swaig.endpoint("Verify insurance status",
    insurance_provider=Parameter("string", "Insurance provider name"),
    member_id=Parameter("string", "Member ID number"),
    date_of_birth=Parameter("string", "Date of birth (YYYY-MM-DD)"))
def verify_insurance(member_id, insurance_provider, date_of_birth):
    if member_id in MOCK_DATA['insurance']:
        return f"Member ID: {member_id}, Provider: {insurance_provider}, Status: active"
    return "Insurance not found"

@swaig.endpoint("Check therapy coverage",
    member_id=Parameter("string", "Member ID number"))
def check_eligibility(member_id):
    if member_id in MOCK_DATA['insurance']:
        services = ', '.join(MOCK_DATA['insurance'][member_id]['services'])
        return f"Covered services: {services}"
    return "No coverage found"

@swaig.endpoint("Schedule therapy session",
    member_id=Parameter("string", "Member ID number"),
    preferred_date=Parameter("string", "Preferred date (YYYY-MM-DD)"),
    preferred_time=Parameter("string", "Preferred time (HH:MM)"),
    therapist_id=Parameter("string", "Therapist ID"))
def schedule_therapy_session(member_id, preferred_date, preferred_time, therapist_id):
    return f"Session scheduled for {preferred_date} at {preferred_time}"

@swaig.endpoint("Get available therapists",
    insurance_provider=Parameter("string", "Insurance provider name"))
def get_therapist_info(insurance_provider):
    therapists = MOCK_DATA['therapists']
    return ", ".join(f"{t['name']} ({t['specialty']})" for t in therapists)

@swaig.endpoint("Get copay information",
    member_id=Parameter("string", "Member ID number"))
def provide_copay_information(member_id):
    if member_id in MOCK_DATA['insurance']:
        copay = MOCK_DATA['insurance'][member_id]['copay']
        return f"Copay amount: ${copay}"
    return "Copay information not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001) 