import docx2txt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image

def retrieve_text():
    result_text = docx2txt.process("./test_data/test_cv.docx")
    # print(result_text)
    return result_text

def retrieve_text_from_image():
    img = Image.open('./test_data/Capture1.PNG')
    text = pytesseract.image_to_string(img)
    print(text)
    return text

retrieve_text_from_image ()