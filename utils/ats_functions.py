import json
import fitz
from PIL import Image
import pytesseract


class Ats_Functions:
    def __init__(self, pdf_file_path, extracted_resume, spacing_function_path):
        # For check_images function
        self.pdf_file_path = pdf_file_path
        
        # For pronoun function
        self.extracted_resume = extracted_resume

        # For analyze_alignment_and_spacing function
        self.spacing_function_path = spacing_function_path


    def check_images(self):
        """
        Required args from class: Path of pdf file
        Returns: boolean value, int value(count of images)
        """
        
        pdf = fitz.open(self.pdf_file_path)
        page = pdf[0]
        images = page.get_images()

        if images:
            return True, images 
        else:
            return False, 0

    def pronoun(self):
        """
        Required args from class: Path to extracted text in json (it has to be
                                    pre-processed, meaning no punctuations)
        Returns: Boolean value, int value(count of pronouns)
        """

        # Reading the extracted words from the resume
        with open(self.extracted_resume, 'r') as json_file:
            data = json.load(json_file)

        pers_pron = ['I', 'We', 'Me', 'My', 'Mine', 'Myself', 'You', 'Your', 'Yours', 'Yourself', 'She', 'Her', 'Hers', 'Herself', 'He', 'Him', 'Himself', 'His', 'They', 'Them', 'Themself', 'Themselves', 'Their', 'Us', 'Our', 'Ourselves', 'Ourself', 'Ours', 'It', 'Itself']
        
        # Extract the text from your JSON data (adjust the key as needed)
        text = data.get('text_field', '')
        lowercase = text.lower().split(" ")

        count = 0

        for pronoun in pers_pron:
            count += lowercase.count(pronoun.lower())

        threshold = 5
        if count >= threshold:
            # Resume rejected
            return False, count
        else:
            # Resume accepted
            return True, count

    def analyze_alignment_and_spacing(self):
        try:
           
            image = Image.open(self.spacing_function_path)

          
            text = pytesseract.image_to_string(image)

           
            lines = text.split('\n')

          
            total_lines = len(lines)
            out_of_place_lines = 0

            for i in range(1, total_lines):
               
                if len(lines[i]) > 0 and len(lines[i-1]) > 0:
                    if abs(len(lines[i]) - len(lines[i-1])) > 10:
                        out_of_place_lines += 1

            alignment_score = (total_lines - out_of_place_lines) / total_lines

            return alignment_score, lines

        except Exception as e:
            return None, str(e)

if __name__ == "__main__":
    # Only to test `analyze_alignment_and_spacing` function
    document_path = "document path"  
    ats = Ats_Functions(document_path)
    alignment_score, lines = ats.analyze_alignment_and_spacing()
    
    if alignment_score is not None:
        print(f"Alignment Score: {alignment_score:.2f}")
        print("Document Lines:")
        for line in lines:
            print(line)
    else:
         print("An error occurred during document analysis.")