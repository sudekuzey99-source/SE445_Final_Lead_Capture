# SE445 Final Lead Capture Project

This repository contains the SE445 Final Project workflow for the Lead Capture to CRM business case.

## Workflow

Webhook/Input → Validation → AI Classification → AI Email Generation → Storage/CRM

## Data Schema

The final lead record follows this structure:
```json
{
  "name": "",
  "email": "",
  "message": "",
  "status": "",
  "intent": "",
  "urgency": ""
}
```

## Project Structure

HW3_Lead_Capture_Base/ : Base HW3 lead capture workflow
validation/ : Part 2 validation logic
classification/ : Part 3 intent and urgency classification
email_generation/ : Part 4 personalized email generation and mock CRM output
screenshots/ : Validation output screenshot
.gitignore : Ignore rules for cache and system files

## Storage

Storage is simulated using mock_crm.csv inside the email_generation folder.

The stored lead data includes:

name
email
message
status
intent
urgency

## Documentation
The Word report should include:

workflow explanation
validation logic
AI classification logic
AI email generation logic
data schema
GitHub repository link
screenshots

## Team Notes
Each project part is organized in a separate folder.

Before making changes, each team member should run:

git pull

After making changes, each team member should commit and push their own part.
