# Therapy Eligibility AI Agent with SignalWire AI Gateway (SWAIG) Integration

## Table of Contents

1. [Introduction](#introduction)
2. [Overview](#overview)
3. [SWAIG Function Schemas](#swaig-function-schemas)
   - [Function: `verify_insurance`](#function-verify_insurance)
   - [Function: `check_eligibility`](#function-check_eligibility)
   - [Function: `schedule_therapy_session`](#function-schedule_therapy_session)
   - [Function: `get_therapist_info`](#function-get_therapist_info)
   - [Function: `provide_copay_information`](#function-provide_copay_information)
4. [Example API Call in SWAIG Format](#example-api-call-in-swaig-format)
5. [Python Code for Mock Functions](#python-code-for-mock-functions)

---

## 1. Introduction

This document outlines the design for a *Therapy Eligibility AI Agent* using the SignalWire AI Gateway (SWAIG) integration. Each API follows the OpenAI Tool Spec schema, allowing the AI to verify insurance details, check eligibility for online therapy, provide copayment information, and schedule a therapy session.

---

## 2. Overview

Each SWAIG function accepts `POST` data in a structured JSON format, including an `argument` field that defines parameters as per OpenAI Tool Spec schema. These functions perform tasks like insurance verification, eligibility confirmation, therapist retrieval, and copay information. 

---

## 3. SWAIG Function Schemas

### Function: `verify_insurance`

- **Purpose**: Verifies the user's insurance information and confirms eligibility for therapy.
- **Schema**:

  ```json
  {
    "function": "verify_insurance",
    "description": "Verify the insurance provider and confirm active status",
    "parameters": {
      "properties": {
        "insurance_provider": {
          "description": "The user's insurance provider name.",
          "type": "string"
        },
        "member_id": {
          "description": "The insurance member ID number.",
          "type": "string"
        },
        "date_of_birth": {
          "description": "The user's date of birth in YYYY-MM-DD format.",
          "type": "string"
        }
      },
      "type": "object"
    }
  }
  ```

### Function: `check_eligibility`

- **Purpose**: Checks if the insurance plan covers online therapy services.
- **Schema**:

  ```json
  {
    "function": "check_eligibility",
    "description": "Check coverage for online therapy under the insurance plan",
    "parameters": {
      "properties": {
        "insurance_provider": {
          "description": "The user's insurance provider name.",
          "type": "string"
        },
        "member_id": {
          "description": "The insurance member ID number.",
          "type": "string"
        }
      },
      "type": "object"
    }
  }
  ```

### Function: `schedule_therapy_session`

- **Purpose**: Schedules an online therapy session based on user eligibility and therapist availability.
- **Schema**:

  ```json
  {
    "function": "schedule_therapy_session",
    "description": "Schedule a therapy session for the user with an eligible therapist",
    "parameters": {
      "properties": {
        " ": {
          "description": "The insurance member ID number for scheduling.",
          "type": "string"
        },
        "preferred_date": {
          "description": "The preferred date for the therapy session in YYYY-MM-DD format.",
          "type": "string"
        },
        "preferred_time": {
          "description": "The preferred time for the therapy session in military time format (HH:MM).",
          "type": "string"
        },
        "therapist_id": {
          "description": "The ID of the therapist for the session.",
          "type": "string"
        }
      },
      "type": "object"
    }
  }
  ```

### Function: `get_therapist_info`

- **Purpose**: Retrieves information about therapists who accept the user's insurance.
- **Schema**:

  ```json
  {
    "function": "get_therapist_info",
    "description": "Retrieve therapists available within the user's insurance network",
    "parameters": {
      "properties": {
        "insurance_provider": {
          "description": "The insurance provider accepted by the therapist.",
          "type": "string"
        }
      },
      "type": "object"
    }
  }
  ```

### Function: `provide_copay_information`

- **Purpose**: Provides copayment details based on the user's insurance coverage.
- **Schema**:

  ```json
  {
    "function": "provide_copay_information",
    "description": "Retrieve copayment amount for therapy sessions",
    "parameters": {
      "properties": {
        "insurance_provider": {
          "description": "The user's insurance provider name.",
          "type": "string"
        },
        "member_id": {
          "description": "The insurance member ID number.",
          "type": "string"
        }
      },
      "type": "object"
    }
  }
  ```

---

## 4. Example API Call in SWAIG Format

Here’s an example of how the `verify_insurance` API might look when a request is made in the SWAIG format:

```json
{
  "ai_session_id": "example-session-id",
  "app_name": "therapy_agent_app",
  "argument": {
    "parsed": [
      {
        "insurance_provider": "Blue Cross Blue Shield",
        "member_id": "123456789",
        "date_of_birth": "1980-01-01"
      }
    ],
    "raw": "{\"insurance_provider\":\"Blue Cross Blue Shield\",\"member_id\":\"123456789\",\"date_of_birth\":\"1980-01-01\"}",
    "substituted": ""
  },
  "parameters": {
    "properties": {
      "insurance_provider": {
        "description": "The user's insurance provider name.",
        "type": "string"
      },
      "member_id": {
        "description": "The insurance member ID number.",
        "type": "string"
      },
      "date_of_birth": {
        "description": "The user's date of birth in YYYY-MM-DD format.",
        "type": "string"
      }
    },
    "type": "object"
  },
  "function": "verify_insurance",
  "description": "Verify the insurance provider and confirm active status",
  "content_type": "text/swaig",
  "meta_data_token": "example-meta-data-token"
}
```

---

## 5. Python Code for Mock Functions

Here’s Python code to mock the therapy AI Agent’s core functions, simulating the behavior as described in the SWAIG schemas.

```python
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

# Execute the mock verify function
print(verify_insurance(example_data))
```

