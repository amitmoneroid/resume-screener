import pdfplumber 
import json

class ResumeExtractor:
    def __init__(self, resume_file):
        self.resume_file = resume_file
        self.extracted_data = {
            'file_name': self.resume_file,
            'data': []
        }
    
    def extract_text(self):
            
        with pdfplumber.open(self.resume_file) as resume:
            for page in resume.pages:
                text = page.extract_text(x_tolerance=2)
                if text:
                    self.extracted_data['data'].append(text)

        return self.extracted_data
    
    def to_json(self):
        return json.dumps(self.extracted_data, indent=4)

# Usage example:
# resume_file_path = "../data/testing2.pdf"
resume_file_path = "../data/Resume-TCET-FORMAT-PKS.pdf"
resume_extractor = ResumeExtractor(resume_file_path)
resume_extractor.extract_text()  # Extract text first

json_data = resume_extractor.to_json()  # Converting to JSON
print(json_data)

