# lead_storage.py — SE445 Final Project, Part 5
# CRM Lead Storage & Final Output
#
# Purpose:
#   Receives the fully enriched lead object (after validation, classification,
#   and email generation) and appends it to a persistent JSON file.
#   Both valid AND invalid leads are stored — invalid leads are never discarded.
#
# Usage:
#   from part5_storage.lead_storage import save_lead, load_leads, clear_leads
#
# Run standalone demo:
#   python3 part5_storage/lead_storage.py

import json
import os
import datetime

# ── Storage file location ─────────────────────────────────────────────────────
STORAGE_FILE = os.environ.get(
    "LEADS_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "processed_leads.json")
)

BASE_FIELDS = ["name", "email", "message", "status", "intent", "urgency"]


def _load_raw():
    """Read the JSON file and return a list."""
    if not os.path.isfile(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return []


def _write_raw(leads):
    """Overwrite the JSON file."""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)


def save_lead(lead):
    """
    Append a single lead to the persistent storage file.

    Parameters
    ----------
    lead : dict
        The fully enriched lead dict coming from the pipeline.

    Returns
    -------
    dict
        The stored lead record (with 'stored_at' added).
    """
    # Guarantee all base fields are present
    record = {field: lead.get(field, "") for field in BASE_FIELDS}

    # Keep validation errors if present
    if "validation_errors" in lead:
        record["validation_errors"] = lead["validation_errors"]

    # Keep any extra fields (generated_email, timestamp, etc.)
    for key, value in lead.items():
        if key not in record:
            record[key] = value

    # Add storage timestamp
    record["stored_at"] = datetime.datetime.now().isoformat(timespec="seconds")

    # Append to file
    existing = _load_raw()
    existing.append(record)
    _write_raw(existing)

    print("  [Part 5] Lead stored — name: {}, status: {}, intent: {}, urgency: {}".format(
        repr(record.get("name")),
        repr(record.get("status")),
        repr(record.get("intent")),
        repr(record.get("urgency")),
    ))
    print("  [Part 5] Total leads in storage: {}".format(len(existing)))

    return record


def load_leads():
    """Return all stored leads as a list of dicts."""
    return _load_raw()


def clear_leads():
    """Reset storage to an empty list (use only in tests)."""
    _write_raw([])
    print("  [Part 5] Storage cleared.")


# ── Standalone demo ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Part 5 — Lead Storage Demo ===\n")

    valid_lead = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "message": "I need help with my account urgently.",
        "status": "Valid",
        "intent": "Support",
        "urgency": "High",
        "generated_email": "Hello Jane Doe,\n\nThank you for your message...",
    }

    invalid_lead = {
        "name": "",
        "email": "not-an-email",
        "message": "",
        "status": "Invalid",
        "validation_errors": [
            "Name is missing or empty.",
            "Email format is invalid.",
            "Message is missing or empty.",
        ],
        "intent": "",
        "urgency": "",
    }

    print("Storing valid lead:")
    save_lead(valid_lead)

    print("\nStoring invalid lead:")
    save_lead(invalid_lead)

    print("\nAll stored leads:")
    for i, lead in enumerate(load_leads(), 1):
        print("  Lead {}: {}".format(i, json.dumps(lead, indent=4)))
