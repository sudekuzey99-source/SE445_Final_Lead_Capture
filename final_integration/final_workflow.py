import sys
import os

# Add the project root to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validation.validation_logic import validate_lead
from classification.ai_classification import classify_lead
from email_generation.generate_email import generate_email

def run_workflow():
    print("=== SE445 End-to-End Integration Workflow ===")

    # 1. Input
    print("\n1. Input")
    input_lead = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "message": "I want to buy the premium subscription ASAP."
    }
    print(input_lead)

    # 2. Validation result
    print("\n2. Validation result")
    validated_lead = validate_lead(input_lead)
    print(f"Status: {validated_lead.get('status')}")
    if validated_lead.get("validation_errors"):
        print(f"Errors: {validated_lead.get('validation_errors')}")

    # 3. Classification result
    print("\n3. Classification result")
    classified_lead = classify_lead(validated_lead)
    print(f"Intent: {classified_lead.get('intent')}")
    print(f"Urgency: {classified_lead.get('urgency')}")

    # 4. Generated email & 5. Saved CRM record
    print("\n4. Generated email & 5. Saved CRM record")
    print("(Calling generate_email(...) which handles both steps)")
    
    # generate_email will print the AI output block and save to mock_crm.csv
    final_result = generate_email(classified_lead)

    print("\n=== Workflow Completed Successfully ===")

if __name__ == "__main__":
    run_workflow()
