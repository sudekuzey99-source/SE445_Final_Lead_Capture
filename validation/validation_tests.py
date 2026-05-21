from validation_logic import validate_lead
import json

def run_tests():
    # 1. Valid lead example
    valid_lead = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "message": "I would like to know more about your software solutions.",
        "status": "",
        "intent": "",
        "urgency": ""
    }
    
    # 2. Invalid lead example
    invalid_lead = {
        "name": "",
        "email": "not-an-email",
        "message": "   ",
        "status": "",
        "intent": "",
        "urgency": ""
    }
    
    print("--- Testing Valid Lead ---")
    result_valid = validate_lead(valid_lead)
    print(json.dumps(result_valid, indent=2))
    
    print("\n--- Testing Invalid Lead ---")
    result_invalid = validate_lead(invalid_lead)
    print(json.dumps(result_invalid, indent=2))

if __name__ == "__main__":
    run_tests()
