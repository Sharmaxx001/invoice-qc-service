#!/usr/bin/env python3
print("🔥 CLI LOADED SUCCESSFULLY")

import argparse
import json
from pathlib import Path
import sys

from src.extractor.extractor import extract_invoice_from_pdf
from src.validator.validator import validate_invoice, summarize_results


def cmd_extract(args):
    pdf_path = Path(args.pdf)

    if not pdf_path.exists():
        print(f"❌ ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)

    print(f"🔍 Extracting invoice from: {pdf_path}")
    extracted = extract_invoice_from_pdf(str(pdf_path))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(extracted, f, indent=4)

    print(f"✅ Extraction completed → Saved to {output_path}")


def cmd_validate(args):
    json_path = Path(args.json)

    if not json_path.exists():
        print(f"❌ ERROR: JSON file not found: {json_path}")
        sys.exit(1)

    with open(json_path, "r") as f:
        invoice_data = json.load(f)

    print(f"🧠 Validating invoice from {json_path}")
    result = validate_invoice(invoice_data)

    summary = summarize_results([result])

    print("\n=== Validation Result ===")
    print(json.dumps(result, indent=4))

    print("\n=== Summary ===")
    print(json.dumps(summary, indent=4))


def cmd_full_run(args):
    pdf_path = Path(args.pdf)
    report_path = Path(args.report)

    if not pdf_path.exists():
        print(f"❌ ERROR: PDF not found: {pdf_path}")
        sys.exit(1)

    print(f"🔍 Extracting + Validating PDF: {pdf_path}")
    extracted = extract_invoice_from_pdf(str(pdf_path))
    result = validate_invoice(extracted)
    summary = summarize_results([result])

    report = {
        "extracted": extracted,
        "result": result,
        "summary": summary,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"✅ Full Run Completed → Report saved to {report_path}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Invoice Extraction + Validation CLI Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Extract command
    extract_p = subparsers.add_parser("extract", help="Extract invoice from PDF")
    extract_p.add_argument("--pdf", required=True, help="Path to PDF file")
    extract_p.add_argument(
        "--output", required=True, help="Where to save extracted JSON"
    )
    extract_p.set_defaults(func=cmd_extract)

    # Validate command
    validate_p = subparsers.add_parser("validate", help="Validate invoice JSON file")
    validate_p.add_argument("--json", required=True, help="Path to invoice JSON file")
    validate_p.set_defaults(func=cmd_validate)

    # Full-run command
    full_p = subparsers.add_parser("full-run", help="Extract + Validate + Save report")
    full_p.add_argument("--pdf", required=True, help="Path to PDF file")
    full_p.add_argument(
        "--report", required=True, help="Where to save final report JSON"
    )
    full_p.set_defaults(func=cmd_full_run)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
