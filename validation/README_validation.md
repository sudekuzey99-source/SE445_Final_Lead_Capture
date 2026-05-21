# Validation Logic for HW3 Lead Capture

This directory contains Part 2 of the project requirements: Validation Logic.

## Files
- `validation_logic.py`: Contains the `validate_lead` function that implements the required checks on incoming lead data.
- `validation_tests.py`: Contains simple test examples to demonstrate the validation behavior for valid and invalid leads.
- `README_validation.md`: This file, documenting the validation component.

## Requirements Implemented
- **Check fields**: Validates the presence of `name`, `email`, and `message` fields.
- **Empty field detection**: Checks if any of the required fields are missing or contain only whitespaces.
- **Email format validation**: Uses regular expressions to ensure the email address is formatted correctly.
- **Validation Status**: Updates the `status` key (which serves as the validation result field) in the lead dictionary, set to either `Valid` or `Invalid`.
- **Validation Errors**: Appends a `validation_errors` key listing all identified error messages if the lead is invalid.
- **Preserve Invalid Leads**: Does not discard invalid leads. Instead, it returns the original lead data alongside the new validation tracking fields so they can be processed or persisted accordingly.

## Usage
To test the validation logic locally, run:
```bash
python validation_tests.py
```
