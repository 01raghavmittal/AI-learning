import nltk
nltk.download('punkt')

import pdfplumber

def extract_pdf_elements(pdf_path):
    elements = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                elements.append({"type": "text", "content": text})
            

            table = page.extract_table()
            if table:
                # Convert table rows to formatted text
                # formatted = "\n".join([" | ".join(row) for row in table])
                elements.append({"type": "table", "content": table})

    return elements


context = extract_pdf_elements('myfile.pdf')
