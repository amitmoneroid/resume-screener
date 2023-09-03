from PyPDF2 import PdfReader
import json

class PDFTextExtractor:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.extracted_data = {
            "file_name": pdf_file,
            "data": []
        }

    def extract_text_from_pdf(self):
        reader = PdfReader(self.pdf_file)

        # Looping through all pages in the PDF
        for page in reader.pages:
            # Extracting text from the page and appending it to the 'data' list
            text = page.extract_text()
            self.extracted_data['data'].append(text)

    def to_json(self):
        return json.dumps(self.extracted_data, indent=4)


pdf_file_path = '../data/Resume-TCET-FORMAT-PKS.pdf'


pdf_extractor = PDFTextExtractor(pdf_file_path)

# Extract text from the PDF
pdf_extractor.extract_text_from_pdf()

json_data = pdf_extractor.to_json()

# Print the JSON data
# print(json_data)