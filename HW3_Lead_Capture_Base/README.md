# HW3 – Better Results – Lead Capture Workflow

## Project Overview
This project is an **upgraded version of the HW2 Lead Capture pipeline**. While HW2 focused on basic connectivity, HW3 introduces a sophisticated validation layer and an automated AI analysis step to ensure high data quality and provide actionable insights for every lead captured.

## Workflow Architecture
The system follows a linear pipeline to process incoming leads:
**Input → Validation → AI Analysis → CRM/Database**

---

## Features & HW3 Enhancements
This version introduces the following improvements over the original HW2 implementation:

- **Advanced Validation System:**
  - **Missing Field Detection:** Automatically identifies if required fields (`name`, `email`, or `message`) are absent.
  - **Email Format Validation:** Uses pattern matching to ensure email addresses are syntactically correct.
- **Improved Data Persistence:**
  - **Invalid Leads Stored:** Unlike simpler systems, invalid leads are **not deleted**. They are preserved in the database for manual review.
  - **Validation Metadata:** Every lead now includes `validation_status` (Valid/Invalid) and `validation_errors` (specific error details).
- **AI-Like Mock Classification:**
  - **Intent Detection:** Categorizes leads into Sales, Support, Partnership, or General.
  - **Urgency Detection:** Assigns a priority level (High, Medium, Low) based on the content.
- **Full CRM/Database Persistence:** All processed data, including validation results and AI insights, is stored in a SQLite database.

---

## API Endpoints
The system exposes two primary endpoints:

- `POST /webhook`: Receives incoming lead data (JSON).
- `GET /api/leads`: Retrieves all captured leads from the database.

---

## How to Run
To run the full workflow, execute these two scripts in separate terminal sessions:

1. **Start the Mock CRM API:**
   ```bash
   python3 mock_crm_api.py
   ```

2. **Start the HW3 Workflow Service:**
   ```bash
   python3 hw3_workflow.py
   ```

---

## Test Examples (via Curl)

### 1. Valid Lead
```bash
curl -X POST http://127.0.0.1:5000/webhook \
-H "Content-Type: application/json" \
-d '{"name": "SE445 Final Project Team", "email": "sude@gmail.com", "message": "I want to buy your product asap!"}'
```

### 2. Missing Email
```bash
curl -X POST http://127.0.0.1:5000/webhook \
-H "Content-Type: application/json" \
-d '{"name": "SE445 Final Project Team", "message": "Need help with my account."}'
```

### 3. Invalid Email Format
```bash
curl -X POST http://127.0.0.1:5000/webhook \
-H "Content-Type: application/json" \
-d '{"name": "SE445 Final Project Team", "email": "wrong-email-format", "message": "Can we discuss a partnership?"}'
```

---

## Screenshots
The following screenshots document the system's performance and are available in the `screenshots/` directory:
- `workflow-running.png`
- `test1-valid-result.png`
- `test2-missing-email.png`
- `test3-invalid-email-format.png`
- `api-leads-browser.png`
- `api-leads-terminal.png`

---

## Conclusion
The HW3 Lead Capture Workflow represents a significant step forward in automated data processing. By integrating validation and mock AI analysis, the system transforms raw input into structured, categorized, and prioritized data. The decision to persist invalid leads ensures that the sales and support teams never miss an opportunity due to a simple typing error, while maintaining a high standard for the "Valid" data entering the CRM.
