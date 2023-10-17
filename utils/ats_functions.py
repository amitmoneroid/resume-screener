import fitz
from PIL import Image

class Ats_Functions:
    def __init__(self,file):
        self.file = file

    def check_images(self):
        """
        Returns: boolean value, int value(count of images)
        """
        pdf = fitz.open(self.file)
        page = pdf[0]
        images = page.get_images()

        if images:
            return True, images 
        else:
            return False, 0
