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

JSON handling
