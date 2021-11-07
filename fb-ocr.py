from PIL import Image
import pytesseract
import settings
import os

pytesseract.pytesseract.tesseract_cmd = settings.DEFAULT_TESSERACT_DIR

ocr_images = os.listdir(settings.DEFAULT_OCR_DIR)
try:
    for i in ocr_images:
        with open(f'{settings.DEFAULT_OCR_DIR}/txt/{i.replace(".png", ".txt")}', 'w',
                  encoding='utf-8') as f:
            image = Image.open(f'{settings.DEFAULT_OCR_DIR}/{i}')
            str_image = pytesseract.image_to_string(image, lang="tur")
            print(str_image, file=f)
except PermissionError as e:
    settings.LOG.error(e)
