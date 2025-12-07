# 📄 Invoice QC Service  
**Automated Invoice Extraction + Validation Pipeline (FastAPI + Python)**  
Internship Assignment — DeepLogicAI (Dec 2025)

---

## 🚀 Overview  

Invoice QC Service is a full-featured pipeline that:

1. **Extracts invoice fields** from PDF files  
2. **Validates the extracted data** against business rules  
3. Provides a **CLI tool** for running the pipeline from terminal  
4. Exposes a **FastAPI-based HTTP service** for automation and integration  
5. Generates **summary reports** of validation outcomes  

This project simulates a real invoice-processing backend, including:

- PDF-based data extraction (without OCR templates)
- Schema enforcement and validation
- Business rule checks
- Batch-level summary generation
- HTTP API for frontend / automation use

---

## 🧱 Architecture

```text
invoice-qc-service/
│
├── src/
│   ├── extractor/
│   │   └── extractor.py          # Extracts invoice fields from PDF
│   ├── validator/
│   │   └── validator.py          # Field-level & business validation logic
│   ├── api.py                    # FastAPI HTTP API
│   ├── cli.py                    # Command-line interface (CLI)
│   ├── manual_extractor_test.py  # Dev script to test extraction
│   └── manual_validator_test.py  # Dev script to test validation
│
├── data/
│   └── sample_pdfs/              # Sample invoice PDFs
│
├── extracted/                    # Extracted JSON outputs
├── reports/                      # Validation reports
└── README.md

🔧 Features
1. PDF Extraction

From each invoice PDF, the extractor attempts to pull:

invoice_id

invoice_date

buyer_name

seller_name

total_amount

tax_amount

total_with_tax

currency

line_items (where possible)

2. Validation Engine

For each invoice, the validator checks:

Required fields present (e.g. invoice_id, buyer_name, seller_name, total_amount, currency)

Format rules (valid date format, valid currency code)

Numeric rules (non-negative totals, numeric types)

Business rules, e.g.:

total_amount ≈ sum of line_items.line_total (within a tolerance)

Each invoice produces a result:

{
  "invoice_id": "...",
  "valid": true/false,
  "errors": [
    "missing_field:buyer_name",
    "bad_format:invoice_date",
    "business_rule:total_mismatch"
  ]
}

3. Batch Summary

Across a list of invoices, a summary is generated:

total_invoices

valid_invoices

invalid_invoices

missing_count_by_field — how many times each required field was missing

4. CLI (Command Line Interface)

Using click, the CLI supports:

extract → PDF → JSON

validate → JSON → validation report

full-run → PDF → extract + validate → full report

5. REST API (FastAPI)

FastAPI service exposes:

GET /health – basic health check

POST /validate-json – validate an array of invoice JSON objects

POST /extract-and-validate-pdf – upload a PDF, extract fields, then validate

6. Interactive API Docs

FastAPI’s built-in Swagger UI at:

http://127.0.0.1:8000/docs


lets you test endpoints via browser.

🛠 Setup & Installation
1. Clone the repository
git clone <YOUR-REPO-URL>
cd invoice-qc-service

2. Python version

Project is tested with Python 3.11.

3. Create and activate virtual environment
py -3.11 -m venv venv311
.\venv311\Scripts\activate


(Use equivalent commands on Mac/Linux.)

4. Install required libraries

Install the dependencies one by one (or group them if you like):

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

▶ Running the FastAPI Server

From the project root (with venv active):

uvicorn src.api:app --reload


The server will start on:

http://127.0.0.1:8000


API docs (Swagger UI):

http://127.0.0.1:8000/docs

🧪 API Usage
1. Health Check

Endpoint:

GET /health


Example response:

{
  "status": "ok",
  "env": "local",
  "version": "v1"
}

2. Validate a List of Invoice JSON Objects

Endpoint:

POST /validate-json
Content-Type: application/json


Request body (example):

[
  {
    "invoice_id": "AUFNR123456",
    "invoice_date": "2024-05-10",
    "buyer_name": "Softwareunternehmen",
    "seller_name": "Unternehmen für Computerteile",
    "total_amount": 216.0,
    "tax_amount": 41.04,
    "total_with_tax": 257.04,
    "currency": "EUR",
    "line_items": [
      {
        "description": "USB-Maus",
        "quantity": 16,
        "unit_price": 4.0,
        "line_total": 64.0
      }
    ]
  }
]


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

