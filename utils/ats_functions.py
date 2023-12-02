import json
import fitz
from PIL import Image
import re 
from nltk.tokenize import RegexpTokenizer
import numpy as np


class Ats_Functions:
    def __init__(self, pdf_file_path, extracted_resume):
        # For check_images function
        self.pdf_file_path = pdf_file_path
        
        # For pronoun function
        self.extracted_resume = extracted_resume

        # Assigns data from the path by loading load_data
        self.load_data()


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

    def load_data(self):
        try: 
            #loads data into the  json.data from the Json file 
            with open(self.extracted_resume, 'r' ) as json_file:
                self.data=json.load(json_file)
        
        #If there appears to be File missing error, prints the statement
        except FileNotFoundError:
            print(f"File not found: {self.path}")
            self.data= None 

    def Count_bullet(text):
    # tokenizer matches all the '•' or '-'
        tokenizer = RegexpTokenizer( r'[*•\-]\s+')
    #lst stores * and • and -
        lst=tokenizer.tokenize(text)
        return len(lst)

    #Checks for: If the user has used appropriate no. of bullet points
    def Check_bullet_point(self):
        ct=self.Count_bullet()

        # Checks if it is within the Resume limit suggestion
        if   ct > 3 and ct < 8:
            return True
        else :                                    
            return False

    # Checks for no. of paragraph
    def Count_Paragraph(self):
        no_of_paragraph=0
        remove_bullet=self.data.split('•')
        
        # Removes bullet and stores the data in data_without_bullet
        data_without_bullet = ''.join(remove_bullet)
        
        remove_hyphen_bullet=data_without_bullet.split('-')
        
        # Removes hyohen and stores the data in data_without_bullet_hyphen
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
        return no_of_paragraph

    # Checks for paragraph
    def IsParagraph(self):
        if self.Count_Paragraph > 0 :
            return True
        else:
            return False
    
    def is_color_acceptable(self, pixel, target_color, threshold):
        # Checks if pixel is in acceptable proximity of target color
        lower_bound = target_color - threshold
        upper_bound = target_color + threshold
        return np.all((pixel >= lower_bound) & (pixel <= upper_bound))

    def check_acceptable_color(self, image, target_color, threshold):
        """
        Description: Calculates the percentage of specified target color in the image
        Returns: Percentage (between 0 and 1) of target color in image
        """
        # Flattening the grid of pixels
        pixels = image.reshape((-1, 3))

        # If color is either red, green or blue, the current color is allowed to vary more.
        if np.array_equal(target_color, (255, 0, 0)) or np.array_equal(target_color, (0, 255, 0)) or np.array_equal(target_color, (0, 0, 255)):
            threshold = 150
        else:
            threshold = 50

        # Boolean array for each pixel matching the target color
        acceptable_pixels = np.array([self.is_color_acceptable(pixel, target_color, threshold) for pixel in pixels])

        total_pixels = pixels.shape[0]

        # Percentage of pixels similar to target color
        acceptable_percentage = np.sum(acceptable_pixels) / total_pixels
        return acceptable_percentage

    def color_check(self):
        """
        Description: Checks colors used in resume and returns score accordingly. Scores colorful resumes less
        Required args: resume pdf path
        Returns: Dictionary of % of each color in the resume. (Goal is to return a score between 0 and 1)
        """
        try:
            # Loading pdf in images
            pdf_document = fitz.open(self.pdf_file_path)
            pdf_images = []
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                images_list = page.get_pixmap()
                width, height = images_list.width, images_list.height
                image_bytes = images_list.samples
                image_np = np.frombuffer(image_bytes, dtype=np.uint8)

                # Turing the images into an grid(array) of pixels each with RGB values
                image_np = image_np.reshape((height, width, -1))
                pdf_images.append(image_np)
        except Exception as e:
            print(f"Error in pdf_to_images: {e}")
            return

        standard_colors = {
            "Black": (0, 0, 0),
            "White": (255, 255, 255),
            "Red": (255, 0, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255),
            "Yellow": (255, 255, 0),
            "Magenta": (255, 0, 255),
            "Cyan": (0, 255, 255),
            "Gray": (128, 128, 128),
            "Purple": (128, 0, 128),
            "Orange": (255, 165, 0),
            "Brown": (165, 42, 42),
        }

        # Dict of percentage of colors
        resume_colors = {key: .0 for key in standard_colors.keys()}

        # Calculating percentage of each color in resume
        for color_name, target_color in standard_colors.items():
            threshold = 150 if color_name in ["Red", "Green", "Blue"] else 50
            color_percentage = self.check_acceptable_color(pdf_images[0], np.array(target_color), threshold)
            resume_colors[color_name] = color_percentage
        
        # Need to make an appropriate method of scoring for colors
        ...
        # For now, just returning a dictionary of percentage of each color
        return resume_colors
