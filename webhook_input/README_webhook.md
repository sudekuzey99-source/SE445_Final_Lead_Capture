# Part 1 – Webhook & Input Handling

This module implements the webhook entry point for the SE445 Final Lead Capture workflow.

## Features

- Receives POST requests
- Accepts JSON payloads
- Handles name, email, and message fields

## Files

- workflow_step1.json
- webhook_documentation.docx
- screenshots/

## Example Input

{
  "name": "Ali",
  "email": "ali@test.com",
  "message": "I need help with your service"
}

## Workflow Role

Webhook/Input → Validation → AI Classification → Email Generation → Storage
