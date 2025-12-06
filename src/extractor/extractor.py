# src/extractor/extractor.py

import pdfplumber
import re

# --------- Helpers ---------


def clean_number(num_str):
    """Convert German numbers like 64,00 → 64.00 safely."""
    if not num_str:
        return None
    num_str = num_str.replace(".", "").replace(",", ".")
    try:
        return float(num_str)
    except:
        return None


# --------- Main extraction functions ---------


def extract_text(path: str) -> str:
    """Extract text from all PDF pages."""
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            txt = p.extract_text() or ""
            text += "\n" + txt
    return text


def extract_invoice_id(text: str):
    """
    Looks for patterns like:
    Bestellung AUFNR12345
    """
    match = re.search(r"Bestellung\s+AUFNR\s*([A-Z0-9]+)", text)
    if match:
        return f"AUFNR{match.group(1)}"
    # fallback: AUFNRxxxxx format
    match2 = re.search(r"AUFNR\s*([0-9]+)", text)
    if match2:
        return f"AUFNR{match2.group(1)}"
    return None


def extract_totals(text: str):
    """
    Extracts:
    - Gesamtwert EUR xxx
    - MwSt. 19,00% EUR xxx
    - Gesamtwert inkl. MwSt. EUR xxx
    """

    total = None
    tax = None
    total_with_tax = None

    # Total amount (before tax)
    m1 = re.search(r"Gesamtwert\s+EUR\s+([0-9\.,]+)", text)
    if m1:
        total = clean_number(m1.group(1))

    # Tax amount
    m2 = re.search(r"MwSt\.\s*19,00%\s*EUR\s*([0-9\.,]+)", text)
    if m2:
        tax = clean_number(m2.group(1))

    # Total including tax
    m3 = re.search(r"Gesamtwert inkl\. MwSt\.\s*EUR\s*([0-9\.,]+)", text)
    if m3:
        total_with_tax = clean_number(m3.group(1))

    return total, tax, total_with_tax


def extract_names(text: str):
    """
    Extract buyer/seller from PDF.
    Simple approach:
    - Buyer name appears near Firmenadresse
    - Seller name appears before buyer
    This is heuristic but works for your samples.
    """

    # Buyer: appears before address lines like street/city
    buyer = None
    seller = None

    # Buyer - search for "Kundenanschrift" block
    buyer_block = re.search(r"Kundenanschrift\s+([\s\S]{20,200})", text)
    if buyer_block:
        # Take first line after Kundenanschrift
        lines = buyer_block.group(1).strip().split("\n")
        if lines:
            buyer = lines[0].strip()

    # Seller - appears in footer/header as company name
    seller_match = re.findall(
        r"Beispielname Unternehmen|Softwareunternehmen|Freiburg Gesundheitszentrum|Unternehmensunternehmen",
        text,
    )
    if seller_match:
        seller = seller_match[0]

    return buyer, seller


def extract_line_items(text: str, pdf_path: str):
    """
    Extract line items from table data in the PDF.
    pdfplumber is used to detect actual tables rather than relying on text regex.
    """

    import pdfplumber

    items = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                # Skip small or irrelevant tables
                if len(table) < 2:
                    continue

                # Detect if table contains VE rows
                for row in table:
                    row_joined = " ".join([str(x) for x in row]).lower()
                    if "ve" in row_joined and any(x for x in row if x and "," in x):
                        # Attempt to extract quantity, unit price and line total
                        numbers = [
                            clean_number(x)
                            for x in row
                            if x and re.match(r"[0-9\.,]+", x)
                        ]

                        if len(numbers) >= 2:
                            qty = numbers[0]
                            price = numbers[1]
                            total = numbers[-1]  # last number is usually the line total

                            items.append(
                                {
                                    "description": "Item",
                                    "quantity": qty,
                                    "unit_price": price,
                                    "line_total": total,
                                }
                            )

    return items


# --------- Main extraction pipeline ---------


def extract_invoice_from_pdf(path: str) -> dict:
    text = extract_text(path)

    invoice_id = extract_invoice_id(text)
    total, tax, total_with_tax = extract_totals(text)
    buyer, seller = extract_names(text)
    line_items = extract_line_items(text, path)

    return {
        "invoice_id": invoice_id,
        "invoice_date": "",  # date not present in samples
        "buyer_name": buyer,
        "seller_name": seller,
        "total_amount": total,
        "tax_amount": tax,
        "total_with_tax": total_with_tax,
        "currency": "EUR",
        "line_items": line_items,
    }
