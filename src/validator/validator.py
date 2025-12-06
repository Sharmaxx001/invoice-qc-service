from dateutil.parser import parse as dateparse
from .schema import REQUIRED_FIELDS, ALLOWED_CURRENCIES, TOTAL_TOLERANCE


def validate_invoice(inv: dict):
    errors = []

    # Required fields
    for f in REQUIRED_FIELDS:
        if not inv.get(f):
            errors.append(f"missing_field:{f}")

    # Date format
    try:
        dateparse(inv.get("invoice_date", ""))
    except:
        errors.append("bad_format:invoice_date")

    # Currency check
    if inv.get("currency") not in ALLOWED_CURRENCIES:
        errors.append("invalid_currency")

    # Business rule: totals
    line_items = inv.get("line_items", [])
    if line_items:
        sum_items = sum(float(i.get("line_total", 0)) for i in line_items)
        if abs(sum_items - float(inv.get("total_amount", 0))) > TOTAL_TOLERANCE:
            errors.append("business_rule:total_mismatch")

    return {
        "invoice_id": inv.get("invoice_id"),
        "valid": len(errors) == 0,
        "errors": errors,
    }


def summarize_results(results):
    total = len(results)
    valid = sum(1 for r in results if r.get("valid"))
    invalid = total - valid

    missing_fields = {}

    for r in results:
        for err in r.get("errors", []):
            if err.startswith("missing_field:"):
                field = err.split(":")[1]
                missing_fields[field] = missing_fields.get(field, 0) + 1

    return {
        "total_invoices": total,
        "valid_invoices": valid,
        "invalid_invoices": invalid,
        "missing_count_by_field": missing_fields,
    }
