import os
import re
from google.cloud import vision

def detect_text_from_image(image_path):
    # Set up the client using the service account key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\vkaru\OneDrive\Desktop\Python\textanalysis3.json'
    
    # Create a client
    client = vision.ImageAnnotatorClient()

    # Load the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Construct an image instance
    image = vision.Image(content=content)

    # Use the client to perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    # Extract the full detected text
    full_text = ''
    if texts:
        for text in texts:
            full_text += text.description + '\n'

    return full_text

def extract_phone_numbers(text):
    # Regular expression pattern for US phone numbers
    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    
    # Find all matches in the text
    phone_numbers = phone_pattern.findall(text)
    
    return phone_numbers

# Path to your image file
image_path = r'C:\Users\vkaru\Downloads\Receipt.jpg'

# Detect text from the image
detected_text = detect_text_from_image(image_path)

# Extract phone numbers
phone_numbers = extract_phone_numbers(detected_text)

# Print the extracted phone numbers

print("Extracted phone numbers:")


print(phone_numbers[0])
