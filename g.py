import os
from google.cloud import vision

import utils

# Set the path to your JSON key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'h.json'


def google_ocr(image_path):
    client = vision.ImageAnnotatorClient()
    try:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
    except Exception as x:
        print(x)

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return None


if __name__ == "__main__":
    image_path = "media/a_pass.jpg"
    extracted_text = google_ocr(image_path)
    print(utils.gpt_validate(extracted_text))
