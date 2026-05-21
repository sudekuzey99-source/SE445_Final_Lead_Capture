def classify_lead(payload):
    """
    Classifies the lead's intent and urgency based on the message content.
    Uses simple keyword-based logic.
    Updates and returns the payload with intent and urgency fields.
    """
    message = payload.get("message", "").lower()
    
    intent = "Unknown"
    urgency = "Medium"
    
    # Intent classification
    if any(word in message for word in ["help", "support", "issue", "broken", "fix"]):
        intent = "Support"
    elif any(word in message for word in ["buy", "purchase", "price", "pricing", "sales"]):
        intent = "Sales"
    elif any(word in message for word in ["collaborate", "partner", "partnership", "join"]):
        intent = "Partnership"
        
    # Urgency classification
    if any(word in message for word in ["urgent", "asap", "immediately", "emergency", "fast"]):
        urgency = "High"
    elif any(word in message for word in ["no rush", "whenever", "low priority", "take your time"]):
        urgency = "Low"
        
    payload["intent"] = intent
    payload["urgency"] = urgency
    
    return payload
