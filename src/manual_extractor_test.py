from src.extractor.extractor import extract_invoice_from_pdf
import os

files = [
    "D:\project1\OneDrive_1_12-5-2025\sample_pdf_1.pdf",
    "D:\project1\OneDrive_1_12-5-2025\sample_pdf_2.pdf",
    "D:\project1\OneDrive_1_12-5-2025\sample_pdf_3.pdf",
    "D:\project1\OneDrive_1_12-5-2025\sample_pdf_4.pdf",
    "D:\project1\OneDrive_1_12-5-2025\sample_pdf_5.pdf",
]

for f in files:
    print("\n---", f, "---")
    result = extract_invoice_from_pdf(f)
    print(result)
