# storage_tests.py — SE445 Final Project, Part 5
# Tests for the CRM Lead Storage module (lead_storage.py)
#
# Run:
#   python3 part5_storage/storage_tests.py
#
# Each test prints PASS or FAIL. Exit code is 0 if all pass, 1 otherwise.

import sys
import os
import json

# Allow running from project root:  python3 part5_storage/storage_tests.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Point the storage module at a temporary test file so real data is untouched
TEST_FILE = "/tmp/_se445_test_leads.json"
os.environ["LEADS_FILE"] = TEST_FILE

from part5_storage.lead_storage import save_lead, load_leads, clear_leads  # noqa: E402

# ── Helpers ───────────────────────────────────────────────────────────────────
passed = 0
failed = 0


def check(label: str, condition: bool):
    global passed, failed
    if condition:
        print(f"  PASS  {label}")
        passed += 1
    else:
        print(f"  FAIL  {label}")
        failed += 1


# ── Test 1: Valid lead is stored correctly ────────────────────────────────────
def test_valid_lead_stored():
    print("\nTest 1 — Valid lead is stored correctly")
    clear_leads()

    lead = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "message": "I need help with my account urgently.",
        "status": "Valid",
        "intent": "Support",
        "urgency": "High",
        "generated_email": "Hello Jane Doe,\n\nThank you for your message.",
    }

    result = save_lead(lead)
    stored = load_leads()

    check("save_lead returns a dict", isinstance(result, dict))
    check("exactly one lead in storage", len(stored) == 1)
    check("name stored correctly", stored[0]["name"] == "Jane Doe")
    check("email stored correctly", stored[0]["email"] == "jane.doe@example.com")
    check("status is Valid", stored[0]["status"] == "Valid")
    check("intent is Support", stored[0]["intent"] == "Support")
    check("urgency is High", stored[0]["urgency"] == "High")
    check("generated_email is preserved", "generated_email" in stored[0])
    check("stored_at timestamp added", "stored_at" in stored[0])


# ── Test 2: Invalid lead stored with validation_errors ────────────────────────
def test_invalid_lead_stored():
    print("\nTest 2 — Invalid lead is stored with validation_errors")
    clear_leads()

    lead = {
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

    result = save_lead(lead)
    stored = load_leads()

    check("save_lead returns a dict", isinstance(result, dict))
    check("exactly one lead in storage", len(stored) == 1)
    check("status is Invalid", stored[0]["status"] == "Invalid")
    check("validation_errors is a list", isinstance(stored[0].get("validation_errors"), list))
    check("validation_errors has 3 entries", len(stored[0]["validation_errors"]) == 3)
    check("name field present (even if empty)", "name" in stored[0])
    check("email field present", "email" in stored[0])
    check("message field present", "message" in stored[0])
    check("intent field present", "intent" in stored[0])
    check("urgency field present", "urgency" in stored[0])


# ── Test 3: Existing leads are preserved when a new lead is added ─────────────
def test_existing_leads_preserved():
    print("\nTest 3 — Existing leads are preserved when new lead is added")
    clear_leads()

    lead_a = {
        "name": "Alice",
        "email": "alice@example.com",
        "message": "I want to buy your product.",
        "status": "Valid",
        "intent": "Sales",
        "urgency": "Medium",
    }
    lead_b = {
        "name": "Bob",
        "email": "bob@example.com",
        "message": "Let's collaborate on a project.",
        "status": "Valid",
        "intent": "Partnership",
        "urgency": "Low",
    }
    lead_c = {
        "name": "Carol",
        "email": "carol@example.com",
        "message": "Fix my issue ASAP.",
        "status": "Valid",
        "intent": "Support",
        "urgency": "High",
    }

    save_lead(lead_a)
    save_lead(lead_b)
    save_lead(lead_c)

    stored = load_leads()

    check("three leads in storage", len(stored) == 3)
    check("first lead name is Alice", stored[0]["name"] == "Alice")
    check("second lead name is Bob", stored[1]["name"] == "Bob")
    check("third lead name is Carol", stored[2]["name"] == "Carol")
    check("Alice intent is Sales", stored[0]["intent"] == "Sales")
    check("Bob intent is Partnership", stored[1]["intent"] == "Partnership")
    check("Carol urgency is High", stored[2]["urgency"] == "High")


# ── Test 4: load_leads returns empty list when no file exists ─────────────────
def test_load_when_empty():
    print("\nTest 4 — load_leads returns empty list on fresh storage")
    clear_leads()

    stored = load_leads()
    check("load_leads returns a list", isinstance(stored, list))
    check("list is empty after clear", len(stored) == 0)


# ── Run all tests ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("SE445 Final Project — Part 5 Storage Tests")
    print("=" * 55)

    test_valid_lead_stored()
    test_invalid_lead_stored()
    test_existing_leads_preserved()
    test_load_when_empty()

    # Clean up temp test file
    if os.path.isfile(TEST_FILE):
        os.remove(TEST_FILE)

    print(f"\n{'=' * 55}")
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 55)
    sys.exit(0 if failed == 0 else 1)
