# src/api.py

from typing import List, Optional

import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel, Field

from src.validator.validator import validate_invoice, summarize_results
from src.extractor.extractor import extract_invoice_from_pdf


API_VERSION = "v1"
APP_ENV = os.getenv("APP_ENV", "local")


# ---------- Pydantic Models with Enhanced Documentation ----------


class LineItem(BaseModel):
    """
    Represents a single line item on an invoice.

    Each line item captures product or service details including description,
    quantity, pricing, and calculated totals.
    """

    description: Optional[str] = Field(
        None,
        description="Human-readable description of the product or service",
        example="Premium Cloud Storage - 1TB Plan",
    )
    quantity: Optional[float] = Field(
        None,
        description="Number of units ordered. Supports decimal values for fractional quantities",
        example=2.0,
        ge=0,
    )
    unit_price: Optional[float] = Field(
        None,
        description="Price per single unit in the invoice currency",
        example=49.99,
        ge=0,
    )
    line_total: Optional[float] = Field(
        None,
        description="Total amount for this line item (quantity × unit_price)",
        example=99.98,
        ge=0,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Professional Consulting Services",
                "quantity": 8.0,
                "unit_price": 150.00,
                "line_total": 1200.00,
            }
        }


class InvoiceIn(BaseModel):
    """
    Complete invoice data structure for validation.

    This model represents a full invoice document including header information,
    financial details, and itemized line items. All fields are optional to support
    partial data extraction scenarios.
    """

    invoice_id: Optional[str] = Field(
        None,
        description="Unique identifier for the invoice (e.g., INV-2024-001)",
        example="INV-2024-12345",
    )
    invoice_date: Optional[str] = Field(
        None,
        description="Date the invoice was issued in ISO 8601 format (YYYY-MM-DD)",
        example="2024-12-06",
    )
    buyer_name: Optional[str] = Field(
        None,
        description="Legal name of the purchasing organization or individual",
        example="Acme Corporation Ltd.",
    )
    seller_name: Optional[str] = Field(
        None,
        description="Legal name of the vendor or service provider",
        example="TechSupply Solutions Inc.",
    )
    total_amount: Optional[float] = Field(
        None,
        description="Subtotal amount before taxes and additional charges",
        example=1500.00,
        ge=0,
    )
    tax_amount: Optional[float] = Field(
        None,
        description="Total tax amount applied to the invoice",
        example=150.00,
        ge=0,
    )
    total_with_tax: Optional[float] = Field(
        None,
        description="Final total including all taxes and charges (total_amount + tax_amount)",
        example=1650.00,
        ge=0,
    )
    currency: Optional[str] = Field(
        None,
        description="Three-letter ISO 4217 currency code",
        example="USD",
        min_length=3,
        max_length=3,
    )
    line_items: Optional[List[LineItem]] = Field(
        None, description="Itemized list of products or services on the invoice"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "invoice_id": "INV-2024-98765",
                "invoice_date": "2024-12-06",
                "buyer_name": "Global Enterprises LLC",
                "seller_name": "Premium Services Inc.",
                "total_amount": 2500.00,
                "tax_amount": 250.00,
                "total_with_tax": 2750.00,
                "currency": "USD",
                "line_items": [
                    {
                        "description": "Software License - Annual",
                        "quantity": 5.0,
                        "unit_price": 400.00,
                        "line_total": 2000.00,
                    },
                    {
                        "description": "Technical Support Package",
                        "quantity": 1.0,
                        "unit_price": 500.00,
                        "line_total": 500.00,
                    },
                ],
            }
        }


class InvoiceResult(BaseModel):
    """
    Validation result for a single invoice.

    Contains the validation outcome and any errors detected during
    the quality control process.
    """

    invoice_id: Optional[str] = Field(
        None,
        description="Invoice identifier from the validated document",
        example="INV-2024-12345",
    )
    valid: bool = Field(
        ...,
        description="True if the invoice passes all validation rules, False otherwise",
        example=True,
    )
    errors: List[str] = Field(
        ...,
        description="List of validation error messages. Empty if valid=True",
        example=[],
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {"invoice_id": "INV-2024-12345", "valid": True, "errors": []},
                {
                    "invoice_id": "INV-2024-67890",
                    "valid": False,
                    "errors": [
                        "Missing required field: buyer_name",
                        "Total amount mismatch: calculated 1500.00 but found 1450.00",
                    ],
                },
            ]
        }


class Summary(BaseModel):
    """
    Aggregated validation statistics across multiple invoices.

    Provides a high-level overview of validation results including
    pass/fail counts and field-level missing data analysis.
    """

    total_invoices: int = Field(
        ...,
        description="Total number of invoices processed in this batch",
        example=10,
        ge=0,
    )
    valid_invoices: int = Field(
        ...,
        description="Number of invoices that passed all validation checks",
        example=8,
        ge=0,
    )
    invalid_invoices: int = Field(
        ...,
        description="Number of invoices that failed one or more validation checks",
        example=2,
        ge=0,
    )
    missing_count_by_field: dict = Field(
        ...,
        description="Dictionary mapping field names to the count of invoices missing that field",
        example={"invoice_id": 0, "buyer_name": 1, "total_amount": 2},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total_invoices": 25,
                "valid_invoices": 22,
                "invalid_invoices": 3,
                "missing_count_by_field": {
                    "invoice_id": 0,
                    "invoice_date": 1,
                    "buyer_name": 2,
                    "total_amount": 1,
                },
            }
        }


class ValidateResponse(BaseModel):
    """
    Complete validation response for batch invoice processing.

    Combines individual invoice validation results with aggregated
    statistics for the entire batch.
    """

    results: List[InvoiceResult] = Field(
        ..., description="Per-invoice validation results with error details"
    )
    summary: Summary = Field(
        ..., description="Aggregated statistics across all processed invoices"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {"invoice_id": "INV-2024-001", "valid": True, "errors": []},
                    {
                        "invoice_id": "INV-2024-002",
                        "valid": False,
                        "errors": ["Missing required field: seller_name"],
                    },
                ],
                "summary": {
                    "total_invoices": 2,
                    "valid_invoices": 1,
                    "invalid_invoices": 1,
                    "missing_count_by_field": {"seller_name": 1},
                },
            }
        }


class ExtractAndValidateResponse(BaseModel):
    """
    Combined extraction and validation response for PDF processing.

    Returns the extracted invoice data alongside validation results,
    allowing you to review both the parsed content and its quality assessment.
    """

    extracted: InvoiceIn = Field(
        ..., description="Invoice data extracted from the uploaded PDF document"
    )
    result: InvoiceResult = Field(
        ..., description="Validation result for the extracted invoice"
    )
    summary: Summary = Field(
        ..., description="Validation statistics (will contain 1 invoice)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "extracted": {
                    "invoice_id": "INV-2024-55555",
                    "invoice_date": "2024-12-06",
                    "buyer_name": "Tech Innovations Ltd.",
                    "seller_name": "Office Supplies Co.",
                    "total_amount": 850.00,
                    "tax_amount": 85.00,
                    "total_with_tax": 935.00,
                    "currency": "USD",
                    "line_items": [
                        {
                            "description": "Office Chairs - Ergonomic",
                            "quantity": 10.0,
                            "unit_price": 85.00,
                            "line_total": 850.00,
                        }
                    ],
                },
                "result": {"invoice_id": "INV-2024-55555", "valid": True, "errors": []},
                "summary": {
                    "total_invoices": 1,
                    "valid_invoices": 1,
                    "invalid_invoices": 0,
                    "missing_count_by_field": {},
                },
            }
        }


# ---------- FastAPI Application with Enhanced Metadata ----------

app = FastAPI(
    title="Invoice Quality Control API",
    version=API_VERSION,
    description="""
## Enterprise-Grade Invoice Validation Platform

The Invoice QC API provides automated quality control and validation for invoice documents.
Extract data from PDFs or validate pre-structured JSON invoice data with comprehensive
error detection and detailed reporting.

### Key Features

* **Automated Validation**: Rule-based validation ensuring data completeness and accuracy
* **PDF Extraction**: OCR and AI-powered data extraction from invoice PDFs
* **Batch Processing**: Validate multiple invoices in a single request
* **Detailed Reporting**: Per-invoice results with aggregated statistics
* **Field-Level Analysis**: Track missing fields across invoice batches

### Common Use Cases

* Accounts Payable automation and invoice processing workflows
* Document verification in financial systems
* Quality assurance for data extraction pipelines
* Compliance checking for invoice data integrity

---
    """,
    contact={
        "name": "Invoice QC API Support",
        "email": "support@invoiceqc.example.com",
    },
    license_info={
        "name": "Proprietary",
    },
    openapi_tags=[
        {"name": "meta", "description": "Service health and operational endpoints"},
        {
            "name": "validation",
            "description": "Invoice validation endpoints for structured JSON data",
        },
        {
            "name": "pdf",
            "description": "PDF processing endpoints for document extraction and validation",
        },
    ],
)


# ---------- API Endpoints ----------


@app.get(
    "/health",
    tags=["meta"],
    summary="Health check endpoint",
    description="""
    Returns the current health status of the Invoice QC API service.
    
    Use this endpoint to verify the service is operational and to retrieve
    runtime environment information and version details. This endpoint is
    suitable for load balancer health checks and monitoring systems.
    """,
    responses={
        200: {
            "description": "Service is healthy and operational",
            "content": {
                "application/json": {
                    "example": {"status": "ok", "env": "production", "version": "v1"}
                }
            },
        }
    },
)
def health():
    return {"status": "ok", "env": APP_ENV, "version": API_VERSION}


@app.post(
    "/validate-json",
    response_model=ValidateResponse,
    tags=["validation"],
    summary="Validate structured invoice data",
    description="""
    Perform comprehensive validation on an array of invoice JSON objects.
    
    This endpoint accepts pre-structured invoice data (e.g., from your database or 
    third-party integrations) and validates each invoice against business rules 
    including required fields, numerical consistency, and data format compliance.
    
    **Validation Rules Include:**
    - Required field presence checks
    - Financial calculation verification (line items, taxes, totals)
    - Data format and type validation
    - Cross-field logical consistency
    
    Returns detailed per-invoice validation results plus aggregated batch statistics
    to help you identify systemic data quality issues.
    """,
    responses={
        200: {
            "description": "Validation completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {"invoice_id": "INV-2024-001", "valid": True, "errors": []},
                            {
                                "invoice_id": "INV-2024-002",
                                "valid": False,
                                "errors": [
                                    "Missing required field: buyer_name",
                                    "Total mismatch: expected 1500.00, found 1450.00",
                                ],
                            },
                        ],
                        "summary": {
                            "total_invoices": 2,
                            "valid_invoices": 1,
                            "invalid_invoices": 1,
                            "missing_count_by_field": {"buyer_name": 1},
                        },
                    }
                }
            },
        },
        400: {
            "description": "Invalid request - empty invoice array",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Request body must be a non-empty JSON array of invoices."
                    }
                }
            },
        },
        422: {
            "description": "Validation error - malformed request body",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "invoices", 0, "total_amount"],
                                "msg": "value is not a valid float",
                                "type": "type_error.float",
                            }
                        ]
                    }
                }
            },
        },
    },
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


@app.post(
    "/extract-and-validate-pdf",
    response_model=ExtractAndValidateResponse,
    tags=["pdf"],
    summary="Extract and validate invoice from PDF",
    description="""
    Upload a PDF invoice document for automated data extraction and validation.
    
    This endpoint combines OCR, AI-powered extraction, and validation into a single
    operation. Upload a PDF invoice file, and receive:
    
    1. **Extracted Data**: All invoice fields parsed from the document
    2. **Validation Result**: Quality control assessment with error details
    3. **Summary Statistics**: Aggregated validation metrics
    
    **Supported Formats:**
    - Standard business invoice PDFs
    - Scanned documents (OCR processing)
    - Multi-page invoices
    
    **Processing Pipeline:**
    1. PDF upload and temporary storage
    2. Text and data extraction using OCR/AI
    3. Structured data parsing into invoice model
    4. Comprehensive validation against business rules
    5. Cleanup and response delivery
    
    Perfect for accounts payable automation, document processing workflows,
    and invoice digitization projects.
    """,
    responses={
        200: {
            "description": "PDF processed successfully with extraction and validation results",
            "content": {
                "application/json": {
                    "example": {
                        "extracted": {
                            "invoice_id": "INV-2024-77777",
                            "invoice_date": "2024-11-15",
                            "buyer_name": "Enterprise Solutions Corp.",
                            "seller_name": "Cloud Services Ltd.",
                            "total_amount": 5000.00,
                            "tax_amount": 500.00,
                            "total_with_tax": 5500.00,
                            "currency": "USD",
                            "line_items": [
                                {
                                    "description": "Cloud Infrastructure - Monthly",
                                    "quantity": 1.0,
                                    "unit_price": 5000.00,
                                    "line_total": 5000.00,
                                }
                            ],
                        },
                        "result": {
                            "invoice_id": "INV-2024-77777",
                            "valid": True,
                            "errors": [],
                        },
                        "summary": {
                            "total_invoices": 1,
                            "valid_invoices": 1,
                            "invalid_invoices": 0,
                            "missing_count_by_field": {},
                        },
                    }
                }
            },
        },
        400: {
            "description": "Invalid file format - only PDF files accepted",
            "content": {
                "application/json": {
                    "example": {"detail": "Only PDF files are supported."}
                }
            },
        },
        422: {
            "description": "Request validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "file"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
    },
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


print("⭐ USING THIS API FILE ⭐")
