import pytesseract
from PIL import Image
   
class Ats_Functions:
    def __init__(self, path):
        self.path = path

    def analyze_alignment_and_spacing(self):
        try:
           
            image = Image.open(self.path)

          
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
         #tried this for the first time and it was great time learning new things AI team is rizzing 😁
