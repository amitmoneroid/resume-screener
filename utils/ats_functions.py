import json
import string
import fitz
from PIL import Image
import re 
from nltk.tokenize import RegexpTokenizer
from fuzzy_scoring_system import FuzzyScoringSystem


class AtsFunctions:
    def __init__(self, pdf_file_path, resume_json_path, raw_extracted_resume=None):
        # For check_images function
        self.pdf_file_path = pdf_file_path
        
        self.resume_json_path = resume_json_path

        # Loading resume json
        try: 
            #loads data into the  json.data from the Json file 
            with open(self.resume_json_path, 'r' ) as json_file:
                self.resume_json=json.load(json_file)
        except FileNotFoundError:
            print(f"File not found: {self.path}")

        # Loading raw extracted resume
        self.raw_extracted_resume = raw_extracted_resume
        # if self.raw_extracted_resume == None:
            # Logic for extracting text from each section of 
            # ...

    def check_images(self):
        """
        Description: Checks for images in resume.
        Required args from class: Path of pdf file
        Returns: float (Score for image in resume. 
                        1 for 0 image, 0.5 for 1 image, 
                        output goes asymptotically close to 0 as 
                        no. of images keep increasing)
        """
        
        pdf = fitz.open(self.pdf_file_path)
        page = pdf[0]
        imgs = page.get_images()
        img_count = len(imgs)

        return 2**(-img_count)

    def pronoun(self):
        """
        Description: Checks for pronoun usage in resume.
        Required args from class: resume json or all text in resume in a single string
        Returns: Float (1 for pronoun count between main threshold,
                        decreasing values [0,1] till soft threshold,
                        0 outside soft threshold)
        """

        pers_pron = ['I', 'We', 'Me', 'My', 'Mine', 'Myself', 'You', 'Your'
                     , 'Yours', 'Yourself', 'She', 'Her', 'Hers', 'Herself'
                     , 'He', 'Him', 'Himself', 'His', 'They', 'Them', 'Themself'
                     , 'Themselves', 'Their', 'Us', 'Our', 'Ourselves', 'Ourself'
                     , 'Ours', 'It', 'Itself']

        # Translator for removing all punctuation
        translator = str.maketrans("", "", string.punctuation)

        # Use translate to remove punctuation 
        text = self.raw_extracted_resume.translate(translator)
        lowercase = text.lower().split(" ")

        pronoun_count = 0
        for pronoun in pers_pron:
            pronoun_count += lowercase.count(pronoun.lower())
        # Fuzzy scoring system
        scoring = FuzzyScoringSystem(pronoun_count
                                     ,main_threshold_lower=0
                                     ,main_threshold_upper=0
                                     ,soft_threshold_lower=0
                                     ,soft_threshold_upper=3)
        
        return scoring.score()

    def resume_length(self):
        """
        Description: Checks for number of characters being used in the resume.
        Required args from class: Path to extracted text in json
        Returns: Boolean value (weather resume passes check)
        """

        extracted_data = [value for section in self.resume_json.values() if isinstance(section, list) for dictionary in section for value in dictionary.values()]
        char = ''.join(map(str, extracted_data))
        #droppin all the special characters and whitespces
        for x in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
            char = char.replace(x,"")
        num_words = len(char)

        # Fuzzy scoring system
        scoring = FuzzyScoringSystem(num_words
                                     ,main_threshold_lower=650
                                     ,main_threshold_upper=675
                                     ,soft_threshold_lower=500
                                     ,soft_threshold_upper=725)

        return scoring.score()

    def Count_bullet(text):
        """
        Description: Counts no. of bullet points in text['*','-','•'].
        """

        # Tokenizer matches all the '•' or '-'
        tokenizer = RegexpTokenizer( r'[*•\-]\s+')
        
        # List stores * and • and -
        lst=tokenizer.tokenize(text)
        return len(lst)

    def Check_bullet_point(self):
        """
        Description: Checks appropriate no. of bullet points
        """
        ct = self.Count_bullet()

        # Fuzzy scoring system
        scoring = FuzzyScoringSystem(ct
                                     ,main_threshold_upper=4
                                     ,main_threshold_lower=8
                                     ,soft_threshold_upper=0
                                     ,soft_threshold_lower=12)

        return scoring.score()

    def Count_Paragraph(self):
        """
        Description: Checks no. of paragraphs used in resume.
        Required args from class: Resume JSON or raw resume text
        Returns: Paragraph score (1 for no paragraphs, 0 for any number of paragraphs)
        """

        no_of_paragraph = 0

        # Removes bullet and stores the data in data_without_bullet
        remove_bullet = self.raw_extracted_resume.split('•')
        data_without_bullet = ''.join(remove_bullet)

        # Removes hyohen and stores the data in data_without_bullet_hyphen
        remove_hyphen_bullet=data_without_bullet.split('-')
        data_without_bullet_hyphen=''.join(remove_hyphen_bullet)

        pattern = r' {2,}|\n'

        # This splits the rest of the data with : If it is a new line or multiple spaces then split
        # It lets u store multiple paragraph and lets u check more than one paragraph from a single string
        isolated_paragraaph=re.split(pattern, data_without_bullet_hyphen)

        for pararaph in isolated_paragraaph:
            # regular expression
            # This pattern splits the string into substring without removing the punctuation marks[unlike sentence tokenization]
            paragraph_pattern = r'[^.!?]*[.!?]'
            sentences = re.findall(paragraph_pattern, pararaph)
            # Check if there are multiple sentences
            if len(sentences) > 1:
                no_of_paragraph=no_of_paragraph+1
        
        return 1 if no_of_paragraph == 0 else 0
