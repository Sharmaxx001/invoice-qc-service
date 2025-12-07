📄 Invoice QC Service — README

A lightweight Invoice Extraction & Validation system built with Python + FastAPI.
Extracts invoice fields from PDFs, validates them with rule-based checks, and generates structured JSON reports.

🚀 Features

PDF Extraction → invoice_id, buyer/seller, totals, tax, currency, line items

Rule-Based Validation → missing fields, format checks, total mismatch, etc.

FastAPI Endpoints for JSON validation & PDF upload

CLI Tool for quick extraction + validation

Structured JSON Reports

Clean folder structure suitable for production

🛠️ Tech Stack

Python 3

FastAPI

pdfplumber

pydantic

uvicorn

argparse (CLI)

📂 Project Structure
src/
├── extractor/ # PDF → structured data
├── validator/ # Rule-based validation
├── api.py # FastAPI service
invoice_qc_cli.py # CLI tool
reports/ # Generated reports
extracted/ # Extracted invoice JSON
requirements.txt

⚙️ Installation
pip install -r requirements.txt

▶️ Running the API
uvicorn src.api:app --reload

Docs auto-generated at:

http://127.0.0.1:8000/docs

🧪 CLI Usage
Extract PDF → JSON
python invoice_qc_cli.py extract --pdf data/sample_pdfs/sample_pdf_1.pdf --output extracted/output1.json

Validate JSON
python invoice_qc_cli.py validate --json extracted/output1.json

Full Pipeline (Extract + Validate + Save Report)
python invoice_qc_cli.py full-run --pdf data/sample_pdfs/sample_pdf_1.pdf --report reports/full_report1.json

📘 API Endpoints
POST /validate-json

Validate a list of invoice JSON objects.

POST /extract-and-validate-pdf

Upload PDF → extract → validate → return full result.

GET /health

Service heartbeat.

✔️ Validation Rules

Required field checks

Date format checks

Currency format checks

Total consistency:

total_amount + tax_amount == total_with_tax

Missing field detection

Summary generation

📝 Sample Output
{
"invoice_id": "AUFNR123456",
"valid": true,
"errors": []
}

🎯 What This Project Demonstrates

Designing modular Python services

Building extraction + validation pipelines

API engineering

Clean code, structure & documentation

CLI tool design

<<<<<<< HEAD
JSON handling
=======

Response (shape):

{
  "results": [
    {
      "invoice_id": "AUFNR123456",
      "valid": true,
      "errors": []
    }
  ],
  "summary": {
    "total_invoices": 1,
    "valid_invoices": 1,
    "invalid_invoices": 0,
    "missing_count_by_field": {}
  }
}

3. Upload PDF → Extract + Validate

Endpoint:

POST /extract-and-validate-pdf
Content-Type: multipart/form-data


Form field:

file: PDF file to validate

Example (curl):

curl -X POST "http://127.0.0.1:8000/extract-and-validate-pdf" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@data/sample_pdfs/sample_pdf_1.pdf"


Response (shape):

{
  "extracted": {
    "invoice_id": "AUFNR123456",
    "invoice_date": "",
    "buyer_name": "Softwareunternehmen",
    "seller_name": "Unternehmen für Computerteile",
    "total_amount": 216.0,
    "tax_amount": 41.04,
    "total_with_tax": 257.04,
    "currency": "EUR",
    "line_items": []
  },
  "result": {
    "invoice_id": "AUFNR123456",
    "valid": true,
    "errors": []
  },
  "summary": {
    "total_invoices": 1,
    "valid_invoices": 1,
    "invalid_invoices": 0,
    "missing_count_by_field": {}
  }
}


(The exact values will depend on the PDF.)

💻 CLI Usage

All commands are run from project root with the venv active.

1. Extract from PDF
python -m src.cli extract data/sample_pdfs/sample_pdf_1.pdf extracted/output1.json


This:

Reads the given PDF

Extracts invoice fields

Saves JSON to extracted/output1.json

2. Validate an Extracted JSON
python -m src.cli validate extracted/output1.json reports/validation1.json


This:

Loads the JSON

Runs all validation rules

Saves a report to reports/validation1.json

3. Full Run: Extract + Validate
python -m src.cli full-run data/sample_pdfs/sample_pdf_1.pdf reports/full_report1.json


This:

Extracts from PDF

Validates extracted invoice

Writes a combined report to reports/full_report1.json

📊 Example Full Report (CLI full-run)
{
  "extracted": {
    "invoice_id": "AUFNR123456",
    "buyer_name": "Softwareunternehmen",
    "seller_name": "Unternehmen für Computerteile",
    "total_amount": 216.0,
    "tax_amount": 41.04,
    "total_with_tax": 257.04,
    "currency": "EUR",
    "line_items": []
  },
  "result": {
    "invoice_id": "AUFNR123456",
    "valid": true,
    "errors": []
  },
  "summary": {
    "total_invoices": 1,
    "valid_invoices": 1,
    "invalid_invoices": 0,
    "missing_count_by_field": {}
  }
}

🧩 Limitations & Future Improvements

Line item extraction is currently heuristic and can be improved with:

Better table detection

Layout-aware parsing

Non-invoice PDFs return many missing-field errors (can be extended to detect non-invoices)

No persistence layer yet (no DB) — all outputs are file-based

No authentication/authorization on API (can be added if needed)

Possible future extensions:

React or Next.js dashboard consuming this API

Database (PostgreSQL) for storing historical invoice validation results

Background processing with Celery / RQ

Webhooks / email notifications on invalid invoices

👤 Author

Name: Sarthak Sharma
Role: Final-year CSE student
Context: Internship assignment — DeepLogicAI (Dec 2025)
Project: Invoice QC Service (Extraction + Validation)

>>>>>>> 04d61581c035f2a4fe41b55cc3c5452b41a94e0f
