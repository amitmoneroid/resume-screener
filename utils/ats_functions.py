import fitz
from PIL import Image

class Ats_Functions:
    def __init__(self,file):
        self.file = file

    def check_images(self):
        pdf = fitz.open(self.file)
        page = pdf[0]
        images = page.get_images()

        if images:
            print(f"Found {len(images)} images")
            print("Resume not acceptable")
        else:
            print("No images found")
            print("Resume acceptable")
