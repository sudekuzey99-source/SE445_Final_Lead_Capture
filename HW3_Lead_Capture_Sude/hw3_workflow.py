import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

CRM_API_URL = "http://localhost:5001/api/leads"

def validate_lead(data):
    """
    Validates the lead data.
    Returns (status, errors)
    """
    errors = []
    
    # Check missing fields
    if not data.get('name'):
        errors.append("Missing field: name")
    if not data.get('email'):
        errors.append("Missing field: email")
    if not data.get('message'):
        errors.append("Missing field: message")
        
    # Validate email format
    email = data.get('email', '')
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Invalid email format")
        
    status = "Valid" if not errors else "Invalid"
    return status, ", ".join(errors)

def classify_lead_mock(message):
    """
    Mock AI Classification based on keywords.
    Returns (intent, urgency)
    """
    if not message:
        return "General", "Low"
        
    message_lower = message.lower()
    
    # Intent classification
    if any(word in message_lower for word in ['help', 'support', 'issue', 'problem', 'error']):
        intent = "Support"
    elif any(word in message_lower for word in ['buy', 'price', 'cost', 'sales', 'order', 'demo']):
        intent = "Sales"
    elif any(word in message_lower for word in ['partner', 'collaboration', 'invest']):
        intent = "Partnership"
    else:
        intent = "General"
        
    # Urgency classification
    if any(word in message_lower for word in ['urgent', 'asap', 'immediately', 'now', 'emergency']):
        urgency = "High"
    elif any(word in message_lower for word in ['soon', 'next week', 'important']):
        urgency = "Medium"
    else:
        urgency = "Low"
        
    return intent, urgency

def send_to_crm(lead_data):
    """
    Sends the processed lead data to the CRM API.
    """
    print(f"[WORKFLOW] Sending to CRM: {lead_data.get('email')}")
    try:
        response = requests.post(CRM_API_URL, json=lead_data)
        if response.status_code == 201:
            print("[WORKFLOW] Successfully synced with CRM.")
            return response.json()
        else:
            print(f"[WORKFLOW] CRM Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("[WORKFLOW] CONNECTION ERROR: Is mock_crm_api.py running on port 5001?")
        return None

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # 1. Receive payload
    payload = request.json
    if not payload:
        return jsonify({"error": "No payload provided"}), 400
        
    print(f"\n[WORKFLOW] New lead received: {payload.get('email', 'N/A')}")
    
    # 2. Validation
    validation_status, validation_errors = validate_lead(payload)
    
    # 3. AI Classification
    intent, urgency = classify_lead_mock(payload.get('message', ''))
    
    # 4. Prepare enriched data
    enriched_data = {
        "name": payload.get('name'),
        "email": payload.get('email'),
        "message": payload.get('message'),
        "validation_status": validation_status,
        "validation_errors": validation_errors,
        "intent": intent,
        "urgency": urgency
    }
    
    # 5. Store in CRM (Store ALL leads)
    crm_response = send_to_crm(enriched_data)
    
    # 6. Respond to source
    return jsonify({
        "status": "success",
        "processed_data": enriched_data,
        "crm_sync": "success" if crm_response else "failed"
    }), 200

if __name__ == '__main__':
    print("HW3 Better Results Workflow starting on port 5000...")
    print("Webhook URL: http://localhost:5000/webhook")
    app.run(port=5000, debug=True, use_reloader=False)
