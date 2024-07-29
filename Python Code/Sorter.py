import os
import re
from google.cloud import vision

def detect_text_from_image(image_path):
    # Set up the client using the service account key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\kaush\OneDrive\Desktop\Python\textanalysis2.json'
    
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


def get_first_line_from_image(image_path):
    # Call the original function to get the full text
    full_text = detect_text_from_image(image_path)

    # Split the full text into lines and get the first line
    first_line = full_text.split('\n')[0] if full_text else 'No text detected.'
    return first_line



def extract_dates(text):
    # Regular expression pattern for various date formats
    date_pattern = re.compile(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{2,4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2} (?:st|nd|rd|th)? [a-zA-Z]+ \d{4}|[a-zA-Z]+ \d{1,2}, \d{4}|[a-zA-Z]+ \d{1,2})\b', re.IGNORECASE)

    # Find all matches in the text
    dates = date_pattern.findall(text)

    # Return all found dates
    return dates

def extract_price(text):
    # Regular expression pattern for price
    price_pattern = re.compile(r'\$\s*\d+(?:,\d+)*(?:\.\d+)?')
    
    # Find all matches in the text
    prices = price_pattern.findall(text)
    
    # Convert prices to float after removing commas
    numeric_prices = [float(price.replace('$','').replace('\n ', '')) for price in prices]
    
    #print(numeric_prices) #(testing case)

    # Find and return the highest price
    if numeric_prices:
        highest_price = max(numeric_prices)
        return f"${highest_price:,.2f}"  # Format with a dollar sign and two decimal places
    else:
        return "No prices found"

def extract_addresses(text):
    # Regular expression pattern for various address formats (horizontal format)
    address_pattern = re.compile(r'\b\d{1,5} [A-Z][A-Za-z]*(?: [A-Z][A-Za-z]*)*(?: [A-Za-z]+)+\b|\b\d{1,5} (?:[A-Za-z]+(?: [A-Za-z]+)*|[A-Za-z]+(?: [A-Za-z]+)*,?) (?:[A-Za-z]+(?: [A-Za-z]+)*),? (?:[A-Za-z]+(?: [A-Za-z]+)*)? (?:[A-Z]{2})? \d{5}(?:-\d{4})?\b', re.IGNORECASE)

    # Find all matches in the text
    addresses = address_pattern.findall(text)

    # Return all found addresses
    return addresses

# Path to your image file
image_path = r'C:\Users\kaush\Downloads\Bosa_Receipt.jpg'

# Detect text from the image
detected_text = detect_text_from_image(image_path)

# Extract price
prices = extract_price(detected_text)

#Extract dates
dates = extract_dates(detected_text)

#Extract adresses
addresses = extract_addresses(detected_text)


# Get and print the first line of text
first_line = get_first_line_from_image(image_path)
print("Establishment Name:", first_line)

# Print the extracted date
print("Date of Purchase:")
print(dates)

#Print the extracted price
print("Amount of Purchase:")
print(prices)

#Print the extracted address
print("Address:")
print(addresses)
