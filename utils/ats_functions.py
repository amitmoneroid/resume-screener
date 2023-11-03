import json
import fitz
from PIL import Image


class Ats_Functions:
    def __init__(self, pdf_file_path, extracted_resume):
        # For check_images function
        self.pdf_file_path = pdf_file_path
        
        # For pronoun function
        self.extracted_resume = extracted_resume


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

    def resume_length(self):
        """
        Required args from class: Path to extracted text in json
        Returns: Boolean value (weather resume passes check)
        """
        threshold_limit = 670  
        #This needs to be updated with the data
        with open(self.extracted_resume, "r") as json_file:
            data = json.load(json_file)
            extracted_data = [value for section in data.values() if isinstance(section, list) for dictionary in section for value in dictionary.values()]
            char = ''.join(map(str, extracted_data))
            #droppin all the special characters and whitespces
            for x in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                char = char.replace(x,"")
        if len(char)>threshold_limit:
            return False
        else:
            return True