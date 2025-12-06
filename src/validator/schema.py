REQUIRED_FIELDS = [
    "invoice_id",
    "invoice_date",
    "buyer_name",
    "seller_name",
    "total_amount",
    "tax_amount",
    "total_with_tax",
    "currency",
]

ALLOWED_CURRENCIES = {"EUR"}

TOTAL_TOLERANCE = 0.01
