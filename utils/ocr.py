import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os
import re

pdf_path = "utils/example.pdf"
image_path = "utils/pdf2img/"  # Output directory for images

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Ensure the output directory exists
os.makedirs(image_path, exist_ok=True)

# Function to convert a PDF page to an image and save it as PNG
def convert_page_to_image(page, output_image_path):
    # Use the function get_pixmap to control the DPI (dots per inch)
    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
    pix.save(output_image_path, "png")

# Iterate through pages and convert to images
for page_number in range(pdf_document.page_count):
    page = pdf_document.load_page(page_number)
    image_filename = f"{image_path}page_{page_number + 1}.png"
    convert_page_to_image(page, image_filename)

# Perform OCR on each image and store extracted text
extracted_text = []

for page_number in range(pdf_document.page_count):
    image_filename = f"{image_path}page_{page_number + 1}.png"
    image = Image.open(image_filename)
    
    # Apply any image preprocessing as needed here
    
    # Perform OCR with Tesseract
    text = pytesseract.image_to_string(image, lang="eng", config="--psm 6")
    extracted_text.append(text)


print(extracted_text)
print()

# Function to remove special characters from a text
def remove_special_characters(text):
    pattern = r'[^A-Za-z0-9\s]'  # This pattern matches anything that is not a letter, digit, or space

    # Use re.sub to replace matches with an empty string
    clean_text = re.sub(pattern, '', text)

    return clean_text

cleaned_text = [remove_special_characters(text) for text in extracted_text]
cleaned_text = [text.replace('\n', ', ') for text in cleaned_text]


print(cleaned_text)

# Close the PDF document after all operations
pdf_document.close()


