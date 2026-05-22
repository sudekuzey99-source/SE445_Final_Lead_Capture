# Part 5 – CRM Lead Storage & Final Output

## Objective

Part 5 is the final stage of the SE445 Lead Capture pipeline.  
It receives the fully enriched lead object produced by Parts 1–4 and
**appends it to a persistent JSON file** so that every lead — whether
valid or invalid — is permanently recorded in the system.

---

## Workflow Position

```
Input / Webhook   (Part 1)
        ↓
Validation Logic  (Part 2)   → adds: status, validation_errors
        ↓
AI Classification (Part 3)   → adds: intent, urgency
        ↓
AI Email Generation (Part 4) → adds: generated_email, timestamp
        ↓
CRM Storage       (Part 5)   → appends to processed_leads.json  ← HERE
```

---

## Input JSON Structure

Every lead entering Part 5 must carry these base fields:

```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "message": "I need help with my account urgently.",
  "status": "Valid",
  "intent": "Support",
  "urgency": "High"
}
```

For **invalid leads**, the structure looks like this:

```json
{
  "name": "",
  "email": "not-an-email",
  "message": "",
  "status": "Invalid",
  "validation_errors": [
    "Name is missing or empty.",
    "Email format is invalid.",
    "Message is missing or empty."
  ],
  "intent": "",
  "urgency": ""
}
```

Any extra fields added by Part 4 (e.g. `generated_email`, `timestamp`)
are automatically preserved.

---

## Output / Storage Format

Leads are stored in `part5_storage/processed_leads.json`:

```json
[
  {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "message": "I need help with my account urgently.",
    "status": "Valid",
    "intent": "Support",
    "urgency": "High",
    "generated_email": "Hello Jane Doe,\n\nThank you...",
    "stored_at": "2025-05-20T14:23:01"
  },
  {
    "name": "",
    "email": "not-an-email",
    "message": "",
    "status": "Invalid",
    "validation_errors": [
      "Name is missing or empty.",
      "Email format is invalid.",
      "Message is missing or empty."
    ],
    "intent": "",
    "urgency": "",
    "stored_at": "2025-05-20T14:23:02"
  }
]
```

---

## Implementation Files

```
part5_storage/
├── __init__.py             # Package init; exports save_lead, load_leads, clear_leads
├── lead_storage.py         # Main module — save_lead(), load_leads(), clear_leads()
├── storage_tests.py        # 4 test scenarios covering all cases
├── processed_leads.json    # Auto-created on first save (do not edit by hand)
└── README_part5.md         # This file
```

---

## Public API

### `save_lead(lead: dict) -> dict`

Appends the lead to `processed_leads.json` and returns the stored record.  
Always adds a `stored_at` ISO timestamp.  
Never overwrites previously stored leads.

### `load_leads() -> list`

Returns all stored lead records as a Python list.

### `clear_leads() -> None`

Resets storage to an empty list (intended for testing only).

---

## How to Run Tests

From the **project root**, run:

```bash
python3 part5_storage/storage_tests.py
```

Expected output:

```
=======================================================
SE445 Final Project — Part 5 Storage Tests
=======================================================

Test 1 — Valid lead is stored correctly
  PASS  save_lead returns a dict
  PASS  exactly one lead in storage
  PASS  name stored correctly
  PASS  email stored correctly
  PASS  status is Valid
  PASS  intent is Support
  PASS  urgency is High
  PASS  generated_email is preserved
  PASS  stored_at timestamp added

Test 2 — Invalid lead is stored with validation_errors
  PASS  save_lead returns a dict
  PASS  exactly one lead in storage
  PASS  status is Invalid
  PASS  validation_errors is a list
  PASS  validation_errors has 3 entries
  PASS  name field present (even if empty)
  PASS  email field present
  PASS  message field present
  PASS  intent field present
  PASS  urgency field present

Test 3 — Existing leads are preserved when new lead is added
  PASS  three leads in storage
  PASS  first lead name is Alice
  PASS  second lead name is Bob
  PASS  third lead name is Carol
  PASS  Alice intent is Sales
  PASS  Bob intent is Partnership
  PASS  Carol urgency is High

Test 4 — load_leads returns empty list on fresh storage
  PASS  load_leads returns a list
  PASS  list is empty after clear

=======================================================
Results: 27 passed, 0 failed
=======================================================
```

---

## How to Run the Standalone Demo

```bash
python3 part5_storage/lead_storage.py
```

---

## How to Run the Full End-to-End Workflow

```bash
python3 final_integration/final_workflow_updated.py
```

This runs both a valid lead and an invalid lead through all 5 parts and
prints the enriched records.  
Then it calls `load_leads()` to show everything stored in `processed_leads.json`.

---

## How Part 5 Connects to Parts 1–4

| Part | Module | Output consumed by Part 5 |
|------|--------|--------------------------|
| 1 | Webhook / Input | `name`, `email`, `message` |
| 2 | `validation/validation_logic.py` | `status`, `validation_errors` |
| 3 | `classification/ai_classification.py` | `intent`, `urgency` |
| 4 | `email_generation/generate_email.py` | `generated_email`, `timestamp` |
| **5** | **`part5_storage/lead_storage.py`** | **Stores everything to JSON** |

Part 5 imports nothing from Parts 1–4 directly. It simply receives
the final dict and stores it, keeping concerns clearly separated.

---

## Design Decisions

- **JSON over CSV** — The existing `mock_crm.csv` (Part 4) stores only
  valid leads; Part 5 uses JSON to store *all* leads uniformly, including
  invalid ones with their error details.
- **Append-only writes** — `save_lead()` always reads the existing file
  before writing, so historical data is never lost.
- **No external dependencies** — Only Python standard library modules
  (`json`, `os`, `datetime`) are used, keeping the module beginner-friendly
  and offline-compatible.
- **Environment variable override** — `LEADS_FILE` env var lets tests use
  a temporary file without touching the real storage.
