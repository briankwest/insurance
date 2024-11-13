from flask import Flask
from dotenv import load_dotenv
import os
import random
import logging
from signalwire_swaig.core import SWAIG, SWAIGArgument

load_dotenv()

logging.getLogger('werkzeug').setLevel(logging.WARNING)

if os.environ.get('DEBUG', False):
    print("Debug mode is enabled")
    debug_pin = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}"
    os.environ['WERKZEUG_DEBUG_PIN'] = debug_pin
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    print(f"Debugger PIN: {debug_pin}")

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
    insurance_provider=SWAIGArgument("string", "Insurance provider name", required=True),
    member_id=SWAIGArgument("string", "Member ID number", required=True),
    date_of_birth=SWAIGArgument("string", "Date of birth (YYYY-MM-DD)", required=True))
def verify_insurance(member_id, insurance_provider, date_of_birth, meta_data_token=None, meta_data=None):
    if member_id in MOCK_DATA['insurance']:
        return f"Member ID: {member_id}, Provider: {insurance_provider}, Status: active", {}
    return "Insurance not found", {}

@swaig.endpoint("Check therapy coverage",
    member_id=SWAIGArgument("string", "Member ID number", required=True))
def check_eligibility(member_id, meta_data_token=None, meta_data=None):
    if member_id in MOCK_DATA['insurance']:
        services = ', '.join(MOCK_DATA['insurance'][member_id]['services'])
        return f"Covered services: {services}", {}
    return "No coverage found", {}

@swaig.endpoint("Schedule therapy session",
    member_id=SWAIGArgument("string", "Member ID number", required=True),
    preferred_date=SWAIGArgument("string", "Preferred date (YYYY-MM-DD)", required=True),
    preferred_time=SWAIGArgument("string", "Preferred time (HH:MM)", required=True),
    therapist_id=SWAIGArgument("string", "Therapist ID", required=True))
def schedule_therapy_session(member_id, preferred_date, preferred_time, therapist_id, meta_data_token=None, meta_data=None):
    return f"Session scheduled for {preferred_date} at {preferred_time}", {}

@swaig.endpoint("Get available therapists",
    insurance_provider=SWAIGArgument("string", "Insurance provider name", required=True))
def get_therapist_info(insurance_provider, meta_data_token=None, meta_data=None):
    therapists = MOCK_DATA['therapists']
    return ", ".join(f"Therapist ID: {t['id']}, Name: {t['name']}, Specialty: {t['specialty']}" for t in therapists), {}

@swaig.endpoint("Get copay information",
    member_id=SWAIGArgument("string", "Member ID number", required=True))
def provide_copay_information(member_id, meta_data_token=None, meta_data=None):
    if member_id in MOCK_DATA['insurance']:
        copay = MOCK_DATA['insurance'][member_id]['copay']
        return f"Copay amount: ${copay}", {}
    return "Copay information not found", {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5001), debug=os.getenv('DEBUG'))
