# Step 4: AI Email Generation

This folder contains the logic for automatically generating customized, AI-driven email responses for validated and classified leads.

## What Step 4 Does
Step 4 takes the classified leads (which already have an identified `intent` and `urgency`) and automatically generates personalized email replies. The goal is to provide immediate, context-aware communication to the user based on their specific needs and how urgent their request is. The generated emails are then logged into a simulated CRM system.

## How `generate_email.py` Works
`generate_email.py` contains the core AI email generation logic. It takes a lead's data as input and dynamically constructs a responsive email by:
- Greeting the user by their name.
- Acknowledging their specific intent (e.g., Support, Sales, Partnership) and urgency (e.g., High, Low).
- Producing a tailored response paragraph based on these classifications (e.g., promising a fast response for high-urgency support, or offering detailed pricing for low-urgency sales).
- Outputting a formatted email ready to be sent.

## How `test_leads.py` is Tested
`test_leads.py` serves as the execution script to demonstrate the email generation workflow. When run, it performs the following steps:
1. It iterates over a predefined list of test leads (such as John Smith for a High-priority Support request, and Emily Johnson for a Low-priority Sales request).
2. It processes each lead through the email generation logic.
3. It prints the generated email block directly to the terminal.
4. It simulates a successful workflow by saving the finalized output to a mock CRM file (`mock_crm.csv`).

To run the tests:
```bash
python3 email_generation/test_leads.py
```

## What the Screenshots Prove
The screenshots stored in the `Screenshoots_sec4/` folder capture the terminal output from running `test_leads.py`. They provide visual proof that:
- The AI logic successfully parses the input lead data and generates dynamic, personalized email text without errors.
- The content of the emails appropriately reflects the dynamically assigned `intent` and `urgency` for each specific user.
- The pipeline correctly completes its run and logs the interaction to `mock_crm.csv`, confirming that the entire Step 4 workflow operates exactly as intended.
