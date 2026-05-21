# generate_email.py — SE445 Final Project, Section 4
# AI Email Generation
# Run: python generate_email.py
# In Antigravity terminal: python generate_email.py

import json, datetime, csv, os, re

# ── Gemini API call ───────────────────────────────────────────────────────────
# In Google Antigravity with real API key, replace call_gemini() body with:
#
#   import google.generativeai as genai
#   genai.configure(api_key=os.environ['GEMINI_API_KEY'])
#   model = genai.GenerativeModel('gemini-1.5-pro')
#   response = model.generate_content(prompt)
#   return response.text
#
# For now, this uses a mock that produces realistic output without an API key.

def call_gemini(prompt: str) -> str:
    """Mock Gemini call — produces realistic email output for testing."""
    name    = re.search(r'Name\s*:\s*(.+)',     prompt)
    intent  = re.search(r'Intent\s*:\s*(\w+)',  prompt)
    urgency = re.search(r'Urgency\s*:\s*(\w+)', prompt)

    n = name.group(1).strip()    if name    else "Customer"
    i = intent.group(1).strip()  if intent  else "General"
    u = urgency.group(1).strip() if urgency else "Medium"

    time_map = {
        "High":   "within a few hours",
        "Medium": "within 1-2 business days",
        "Low":    "at a convenient time",
    }
    tone_map = {
        "Support":     "We completely understand your situation and have flagged this as a priority.",
        "Sales":       "We would be happy to provide you with detailed information and pricing.",
        "Partnership": "We are excited about the possibility of working together with your team.",
    }
    time_phrase = time_map.get(u, "shortly")
    tone_line   = tone_map.get(i, "We will be happy to assist you.")

    return (
        f"Hello {n},\n\n"
        f"Thank you for your message.\n\n"
        f"We identified your request as {i} with {u} priority.\n"
        f"{tone_line} A specialist will contact you {time_phrase}.\n\n"
        f"Our team will contact you shortly.\n\n"
        f"Best regards,\nTeam"
    )


# ── Validation ────────────────────────────────────────────────────────────────
def validate_lead(lead: dict) -> tuple:
    if not lead.get("name", "").strip() or len(lead["name"].strip()) < 2:
        return False, "name is missing or too short"
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", lead.get("email", "")):
        return False, "invalid email format"
    if not lead.get("message", "").strip() or len(lead["message"].strip()) < 5:
        return False, "message too short (min 5 chars)"
    if lead.get("intent") not in {"Support", "Sales", "Partnership"}:
        return False, f"intent must be Support | Sales | Partnership, got: {lead.get('intent')}"
    if lead.get("urgency") not in {"High", "Medium", "Low"}:
        return False, f"urgency must be High | Medium | Low, got: {lead.get('urgency')}"
    return True, "ok"


# ── Prompt builder ────────────────────────────────────────────────────────────
def build_prompt(lead: dict) -> str:
    return (
        f"Write a personalized email for:\n"
        f"  Name    : {lead['name']}\n"
        f"  Intent  : {lead['intent']}\n"
        f"  Urgency : {lead['urgency']}\n"
        f"  Message : {lead['message']}\n\n"
        f"Use this exact format:\n"
        f"  Hello {lead['name']},\n"
        f"  Thank you for your message.\n"
        f"  We identified your request as {lead['intent']} with {lead['urgency']} priority.\n"
        f"  [1-2 sentences tailored to intent and urgency]\n"
        f"  Our team will contact you shortly.\n"
        f"  Best regards,\n"
        f"  Team"
    )


# ── Mock CRM save (CSV) ───────────────────────────────────────────────────────
CRM_FILE = os.path.join(os.path.dirname(__file__), "mock_crm.csv")
CRM_COLS = ["name", "email", "message", "status", "intent", "urgency",
            "generated_email", "timestamp"]

def save_to_crm(lead: dict):
    file_exists = os.path.isfile(CRM_FILE)
    with open(CRM_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CRM_COLS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: lead.get(k, "") for k in CRM_COLS})
    print(f"  [CRM] Saved to {CRM_FILE}")


# ── Main pipeline function (Section 4 step) ───────────────────────────────────
def generate_email(lead: dict) -> dict:
    print(f"\n{'='*55}")
    print(f"[Section 4] Processing lead: {lead.get('name')}")

    # Step 1: Validate
    valid, reason = validate_lead(lead)
    lead["status"] = "valid" if valid else "invalid"
    if not valid:
        print(f"  [SKIP] Validation failed: {reason}")
        return lead

    # Step 2: Build dynamic prompt
    prompt = build_prompt(lead)

    # Step 3: Call Gemini (mock for testing)
    print("  [AI]  Calling Gemini 3 Pro...")
    email_body = call_gemini(prompt)
    lead["generated_email"] = email_body
    lead["timestamp"]       = datetime.datetime.now().isoformat(timespec="seconds")

    # Step 4: Print output (screenshot this)
    print("\n--- GENERATED EMAIL ---")
    print(email_body)
    print("-----------------------")

    # Step 5: Save to mock CRM
    save_to_crm(lead)

    return lead


# ── Run both test cases when script is executed directly ──────────────────────
if __name__ == "__main__":
    test_leads = [
        {   # Email Output 1 — Support / High
            "name":    "John Smith",
            "email":   "john.smith@company.com",
            "message": "I need help with my account, this is urgent.",
            "status":  "valid",
            "intent":  "Support",
            "urgency": "High",
        },
        {   # Email Output 2 — Sales / Low
            "name":    "Emily Johnson",
            "email":   "emily.johnson@startup.io",
            "message": "I want to buy your product for our team.",
            "status":  "valid",
            "intent":  "Sales",
            "urgency": "Low",
        },
    ]
    for lead in test_leads:
        generate_email(lead)
    print("\n[DONE] Check mock_crm.csv for saved records.")
