#! pip install pymupdf
import fitz  

doc = fitz.open("data/Executive_Report_DWS_October_2025.pdf")
print(doc.page_count)

