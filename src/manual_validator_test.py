from src.validator.validator import validate_invoice

good_invoice = {
    "invoice_id": "AUFNR123456",
    "invoice_date": "2024-05-22",
    "buyer_name": "Softwareunternehmen",
    "seller_name": "Unternehmen für Computerteile",
    "total_amount": 216.00,
    "tax_amount": 41.04,
    "total_with_tax": 257.04,
    "currency": "EUR",
    "line_items": [
        {
            "description": "USB-Maus",
            "quantity": 16.0,
            "unit_price": 4.0,
            "line_total": 64.0,
        },
        {
            "description": "LED-Monitore 12'",
            "quantity": 16.0,
            "unit_price": 7.5,
            "line_total": 120.0,
        },
        {
            "description": "mechanische Tastatur",
            "quantity": 16.0,
            "unit_price": 2.0,
            "line_total": 32.0,
        },
    ],
}

bad_invoice = {
    "invoice_id": "",
    "invoice_date": "not-a-date",
    "buyer_name": "",
    "seller_name": "Some Seller",
    "total_amount": 9999,
    "tax_amount": -10,
    "total_with_tax": 10000,
    "currency": "ABC",
    "line_items": [],
}

print("GOOD:", validate_invoice(good_invoice))
print("BAD:", validate_invoice(bad_invoice))
