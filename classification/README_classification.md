# Step 3: AI Classification

This folder contains the logic for classifying lead intent and urgency based on their messages.

## Files
- `ai_classification.py`: Contains the `classify_lead(payload)` function, which uses keyword-based detection to populate the `intent` and `urgency` fields of the lead JSON schema.
- `classification_tests.py`: Unit tests validating the classification logic for various intents (Support, Sales, Partnership) and urgencies (High, Medium, Low).
- `README_classification.md`: This file.

## Logic
The classification is based on simple keyword matching:
- **Intent**:
  - `Support`: Keywords like "help", "support", "issue"
  - `Sales`: Keywords like "buy", "purchase", "price"
  - `Partnership`: Keywords like "collaborate", "partner"
- **Urgency**:
  - `High`: Keywords like "urgent", "asap", "immediately"
  - `Low`: Keywords like "no rush", "whenever"
  - `Medium`: Default if neither high nor low is detected.

The original fields (`name`, `email`, `message`, `status`) remain untouched.
