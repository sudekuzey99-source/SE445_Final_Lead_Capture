import re

def validate_lead(lead):
    """
    Validates lead fields: name, email, message.
    Returns the lead with 'status' and 'validation_errors'.
    Invalid leads are not discarded; original data is preserved.
    """
    errors = []
    
    # Check for name
    name = lead.get("name", "")
    if not name or str(name).strip() == "":
        errors.append("Name is missing or empty.")
        
    # Check for email
    email = lead.get("email", "")
    if not email or str(email).strip() == "":
        errors.append("Email is missing or empty.")
    else:
        # Regex for basic email format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, str(email).strip()):
            errors.append("Email format is invalid.")
            
    # Check for message
    message = lead.get("message", "")
    if not message or str(message).strip() == "":
        errors.append("Message is missing or empty.")
        
    # Create the validated lead dictionary keeping original data
    validated_lead = dict(lead)
    
    if errors:
        validated_lead["status"] = "Invalid"
        validated_lead["validation_errors"] = errors
    else:
        validated_lead["status"] = "Valid"
        validated_lead["validation_errors"] = []
        
    return validated_lead
