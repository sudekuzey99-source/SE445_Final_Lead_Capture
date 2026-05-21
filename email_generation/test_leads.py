# test_leads.py — SE445 Final Project, Section 4
# Sends 2 test leads through the email generation pipeline.
# Run: python test_leads.py
# Screenshot the terminal output — those are your 2 email output deliverables.

from generate_email import generate_email

leads = [
    {   # Email Output 1 — Support / High Urgency
        "name":    "John Smith",
        "email":   "john.smith@company.com",
        "message": "I need help with my account, this is urgent.",
        "status":  "valid",
        "intent":  "Support",
        "urgency": "High",
    },
    {   # Email Output 2 — Sales / Low Urgency
        "name":    "Emily Johnson",
        "email":   "emily.johnson@startup.io",
        "message": "I want to buy your product for our team.",
        "status":  "valid",
        "intent":  "Sales",
        "urgency": "Low",
    },
]

for lead in leads:
    generate_email(lead)

print("\n[DONE] 2 emails generated. Screenshot each '--- GENERATED EMAIL ---' block.")
