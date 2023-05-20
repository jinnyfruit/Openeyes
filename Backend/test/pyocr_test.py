import sys
import os
import pyocr
import pyocr.builders

from PIL import Image

if __name__ == '__main__':
    this_program_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_program_directory)

    tesseract_home = "C:\\Program Files\\Tesseract-OCR"
    if tesseract_home not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + tesseract_home

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("OCR tool is not found in path(" + tesseract_home + ")")
        sys.exit(1)

    tool = tools[0]

    img_path = "test.png"
    wk_builder = pyocr.builders.DigitBuilder()
    ocr_results = tool.image_to_string(
        Image.open(img_path),
        lang='eng',
        builder=wk_builder
    )

    print(ocr_results)
    input("Please Enter to Exit")
