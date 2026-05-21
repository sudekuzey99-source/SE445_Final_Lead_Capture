# Final Integration

This folder contains the complete end-to-end integration for the SE445 Final Lead Capture project.

## Files Created
1. `final_workflow.py`: The python script that ties all modules together.
2. `README_final_integration.md`: This documentation file.

## The End-to-End Workflow
The `final_workflow.py` script takes a sample lead and passes it sequentially through the entire pipeline:
1. **Webhook/Input**: A raw sample lead (name, email, message) is initialized.
2. **Validation**: The lead is validated using `validate_lead()` from the `validation` module.
3. **AI Classification**: The valid lead is categorized for `intent` and `urgency` using `classify_lead()` from the `classification` module.
4. **AI Email Generation**: A customized response email is produced via `generate_email()` from the `email_generation` module.
5. **Storage/CRM**: The fully populated lead (with intent, urgency, and generated email) is appended to a `mock_crm.csv` file.

## How to Run
From the root of your project folder, run:
```bash
python3 final_integration/final_workflow.py
```
This will print a clear, step-by-step trace of the data as it moves from input to the CRM storage.
