# src/api.py

from typing import List, Optional

import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel

from src.validator.validator import validate_invoice, summarize_results
from src.extractor.extractor import extract_invoice_from_pdf

from fastapi.middleware.cors import CORSMiddleware


API_VERSION = "v1"
APP_ENV = os.getenv("APP_ENV", "local")


# ---------- Pydantic models ----------


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    line_total: Optional[float] = None


class InvoiceIn(BaseModel):
    invoice_id: Optional[str] = None
    invoice_date: Optional[str] = None
    buyer_name: Optional[str] = None
    seller_name: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    total_with_tax: Optional[float] = None
    currency: Optional[str] = None
    line_items: Optional[List[LineItem]] = None


class InvoiceResult(BaseModel):
    invoice_id: Optional[str]
    valid: bool
    errors: List[str]


class Summary(BaseModel):
    total_invoices: int
    valid_invoices: int
    invalid_invoices: int
    missing_count_by_field: dict


class ValidateResponse(BaseModel):
    results: List[InvoiceResult]
    summary: Summary


class ExtractAndValidateResponse(BaseModel):
    extracted: InvoiceIn
    result: InvoiceResult
    summary: Summary


# ---------- FastAPI app ----------

app = FastAPI(
    title="Invoice QC API",
    version=API_VERSION,
    description="Service for validating extracted invoice data.",
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "env": APP_ENV, "version": API_VERSION}


# ---------- JSON validation ----------


@app.post(
    "/validate-json",
    response_model=ValidateResponse,
    tags=["validation"],
    summary="Validate a list of invoice JSON objects",
    description="Takes an array of invoices and returns per-invoice validation plus a batch summary.",
)
def validate_json(invoices: List[InvoiceIn]):
    if not invoices:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must be a non-empty JSON array of invoices.",
        )

    invoice_dicts = [inv.dict(exclude_unset=True) for inv in invoices]
    results_raw = [validate_invoice(i) for i in invoice_dicts]
    summary_raw = summarize_results(results_raw)

    # Map raw dicts → Pydantic models
    results = [InvoiceResult(**r) for r in results_raw]
    summary = Summary(**summary_raw)

    return ValidateResponse(results=results, summary=summary)


# ---------- PDF upload: extract + validate ----------


@app.post(
    "/extract-and-validate-pdf",
    response_model=ExtractAndValidateResponse,
    tags=["pdf"],
    summary="Upload a PDF invoice, extract fields and validate",
    description="Accepts a single PDF file, runs the extraction pipeline, then validates the extracted invoice.",
)
async def extract_and_validate_pdf(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    # Save uploaded file to a temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        extracted_dict = extract_invoice_from_pdf(tmp_path)
        result_raw = validate_invoice(extracted_dict)
        summary_raw = summarize_results([result_raw])

        extracted = InvoiceIn(**extracted_dict)
        result = InvoiceResult(**result_raw)
        summary = Summary(**summary_raw)

        return ExtractAndValidateResponse(
            extracted=extracted,
            result=result,
            summary=summary,
        )
    finally:
        # Clean up temp file
        try:
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
