import json
import click

from src.extractor.extractor import extract_invoice_from_pdf
from src.validator.validator import validate_invoice, summarize_results


@click.group()
def cli():
    """Invoice QC CLI Tool"""
    pass


# ---------------------- EXTRACT ----------------------
@cli.command()
@click.argument("pdf_path")
@click.argument("output_json")
def extract(pdf_path, output_json):
    """Extract invoice from PDF and save as JSON."""
    result = extract_invoice_from_pdf(pdf_path)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    click.echo(f"Extracted invoice saved to {output_json}")


# ---------------------- VALIDATE ----------------------
@cli.command()
@click.argument("input_json")
@click.argument("report_json")
def validate(input_json, report_json):
    """Validate extracted invoice JSON."""
    with open(input_json, "r", encoding="utf-8") as f:
        invoice = json.load(f)

    result = validate_invoice(invoice)
    summary = summarize_results([result])

    report = {
        "result": result,
        "summary": summary,
    }

    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    click.echo(f"Validation report saved to {report_json}")


# ---------------------- FULL RUN ----------------------
@cli.command()
@click.argument("pdf_path")
@click.argument("report_json")
def full_run(pdf_path, report_json):
    """Extract + Validate in one step."""
    extracted = extract_invoice_from_pdf(pdf_path)
    result = validate_invoice(extracted)
    summary = summarize_results([result])

    report = {
        "extracted": extracted,
        "result": result,
        "summary": summary,
    }

    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    click.echo(f"Full report saved to {report_json}")


if __name__ == "__main__":
    cli()
