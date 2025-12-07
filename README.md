📄 Invoice QC Service — README

A lightweight Invoice Extraction & Validation system built with Python + FastAPI.
Extracts invoice fields from PDFs, validates them with rule-based checks, and generates structured JSON reports.

⭐ 1. Overview

This project implements a complete backend pipeline for Invoice Quality Control (Invoice-QC).
It simulates a real-world system used in Accounts Payable automation workflows.

✔ What this project does

- Extracts structured invoice data from PDF files
- Validates invoice fields using rule-based business logic
- Provides a CLI tool (extract, validate, full-run)
- Exposes a REST API (FastAPI) for automation
- Generates summary validation reports

⭐ 2. Schema & Validation Design

📌 Invoice Fields Chosen

| Field            | Description                          |
| ---------------- | ------------------------------------ |
| `invoice_id`     | Unique identifier for the invoice    |
| `invoice_date`   | Date in YYYY-MM-DD format            |
| `buyer_name`     | Name of the buyer company            |
| `seller_name`    | Name of the seller company           |
| `total_amount`   | Subtotal before tax                  |
| `tax_amount`     | Tax value                            |
| `total_with_tax` | Grand total after tax                |
| `currency`       | 3-letter ISO code (USD/EUR/INR etc.) |
| `line_items`     | List of purchased items              |

🧮 Validation Rules Implemented

| Rule Type           | Description                                                 | Rationale                       |
| ------------------- | ----------------------------------------------------------- | ------------------------------- |
| Required fields     | invoice_id, buyer_name, seller_name, total_amount, currency | Minimum required for processing |
| Date format check   | Must be valid ISO date                                      | Avoids corrupted formats        |
| Numeric validation  | Amounts must be ≥ 0                                         | Prevents invalid totals         |
| Business rule       | `total_amount ≈ sum(line_total)`                            | Ensures item consistency        |
| Tax rule            | `total_with_tax = total_amount + tax_amount`                | Prevents mismatched totals      |
| Line item structure | Description, quantity, unit_price, line_total               | Ensures clean structured data   |

✔ Output of validation

Each invoice returns:
{
"invoice_id": "INV123",
"valid": false,
"errors": [
"missing_field:buyer_name",
"business_rule:total_mismatch"
]
}

⭐ 3. Architecture

📁 Folder Structure

invoice-qc-service/
├── src/
│ ├── extractor/
│ │ └── extractor.py # Extracts invoice fields from PDF
│ ├── validator/
│ │ └── validator.py # Validation engine
│ ├── api.py # FastAPI service
│ ├── cli.py # CLI commands
│ ├── manual_extractor_test.py
│ └── manual_validator_test.py
│
├── data/
│ └── sample_pdfs/
│
├── extracted/ # Extracted JSON files
├── reports/ # Validation reports
└── README.md

⭐ 4. System Flow Diagram

Mermaid Flow Diagram

flowchart LR
A[PDF Files] --> B[Extraction Engine]
B --> C[Extracted JSON]
C --> D[Validation Engine]
D --> E[Results + Errors]
E --> F[Reports / CLI Output]
C --> G[API Response - Extract]
D --> H[API Response - Validate]

⭐ 5. Setup & Installation
🐍 Python Version
Python 3.11.x (project tested on this version)

📦 Create Virtual Environment
py -3.11 -m venv venv
.\venv\Scripts\activate

📚 Install Dependencies
pip install fastapi==0.110.0
pip install uvicorn==0.30.0
pip install pydantic==2.7.1
pip install pydantic-settings==2.2.1
pip install pdfplumber==0.7.6
pip install python-dateutil==2.8.2
pip install pandas==2.2.0
pip install click==8.1.7
pip install python-dotenv==1.0.0
pip install python-multipart
pip install pytest==7.4.0

⭐ 6. Running the Application

▶ Start FastAPI Server
uvicorn src.api:app --reload
UI:
👉 http://127.0.0.1:8000/docs

🧪 Run CLI Commands
1️⃣ Extract from PDF
python -m src.cli extract data/sample_pdfs/sample.pdf extracted/output.json

2️⃣ Validate extracted JSON
python -m src.cli validate extracted/output.json reports/validation.json

3️⃣ Full pipeline (extract + validate)
python -m src.cli full-run data/sample_pdfs/sample.pdf reports/full_report.json

⭐ 7. API Usage
✔ Health Check
GET /health
{ "status": "ok", "env": "local", "version": "v1" }

✔ Validate JSON
POST /validate-json
Request body:
[
{
"invoice_id": "INV123",
"buyer_name": "ABC Corp",
"seller_name": "XYZ Ltd",
"total_amount": 200,
"currency": "USD"
}
]

✔ Extract + Validate PDF
POST /extract-and-validate-pdf (multipart/form-data)

Upload a PDF → response includes:

- Extracted fields
- Validation result
- Summary statistics

⭐ 8. AI Usage Notes

AI tools (ChatGPT / Claude) were used responsibly for:

- Improving documentation clarity
- Generating sample data models
- Debugging extraction and validation logic
- Refining README structure

However:

- All core code (extractor, validator, CLI, API) was understood and written by me
- AI suggestions were manually validated, corrected, and adapted
- No AI-generated code was used blindly

⭐ 9. Assumptions & Limitations

✔ Assumptions - PDFs follow reasonable invoice formatting - Line items are either simple or absent - No OCR required for handwritten or extremely noisy PDFs

✔ Known Limitations

| Limitation                   | Explanation                       |
| ---------------------------- | --------------------------------- |
| Limited line-item extraction | Not fully layout-aware            |
| No database                  | Everything is file-based          |
| No authentication            | API is open locally               |
| Non-invoice PDFs             | Produce many missing-field errors |
| No UI / frontend             | Only Swagger UI provided          |

⭐ 10. Future Improvements

- Build a React/Next.js UI Dashboard
- Add PostgreSQL database for persistence
- Improve line-item extraction (OCR + layout algorithms)
- Add authentication / JWT
- Add background processing with Celery

PROJECT SCREENSHOTS:

1. extraction:
   invoice-qc-service\screenshots\cli_extract.png.jpg

2. Full working:
   invoice-qc-service\screenshots\cli-fullpipeline.png.jpg

3. API CALL:
   invoice-qc-service\screenshots\pdf_extarction.jpg

4. Response:
   invoice-qc-service\screenshots\response.jpg

👤 Author

Name: Sarthak Sharma
Role: Final-year CSE student
Context: Internship assignment — DeepLogicAI (Dec 2025)
Project: Invoice QC Service (Extraction + Validation)
