import cv2
import numpy as np
import fitz
import logging

def setup_logging():
    logging.basicConfig(filename='color_analysis.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pdf_to_images(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        images = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            images_list = page.get_pixmap()
            width, height = images_list.width, images_list.height
            image_bytes = images_list.samples
            image_np = np.frombuffer(image_bytes, dtype=np.uint8)

            # Reshape
            image_np = image_np.reshape((height, width, -1))

            images.append(image_np)
        return images
    except Exception as e:
        logging.error(f"Error in pdf_to_images: {e}")
        return []

def is_color_acceptable(pixel, target_color, threshold):
    lower_bound = target_color - threshold
    upper_bound = target_color + threshold
    return np.all((pixel >= lower_bound) & (pixel <= upper_bound))

def check_acceptable_color(image, target_color, threshold):
    pixels = image.reshape((-1, 3))

    # Change here too
    if np.array_equal(target_color, (255, 0, 0)) or np.array_equal(target_color, (0, 255, 0)) or np.array_equal(target_color, (0, 0, 255)):
        threshold = 150
    else:
        threshold = 50

    acceptable_pixels = np.array([is_color_acceptable(pixel, target_color, threshold) for pixel in pixels])

    total_pixels = pixels.shape[0]
    acceptable_percentage = np.sum(acceptable_pixels) / total_pixels * 100
    return acceptable_percentage

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

if __name__ == "__main__":
    setup_logging()
    resume_pdf_path = r'uploads\Resume-TCET-FORMAT-PKS.pdf'
    pdf_images = pdf_to_images(resume_pdf_path)
    
    for color_name, target_color in standard_colors.items():

        threshold = 150 if color_name in ["Red", "Green", "Blue"] else 50 # Threshold for Red, Green, and Blue colors needs to be changed Line40
        color_percentage = check_acceptable_color(pdf_images[0], np.array(target_color), threshold)
        print(f"Percentage of acceptable {color_name} color: {color_percentage:.2f}%")
