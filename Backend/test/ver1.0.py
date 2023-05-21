import sys
import os
import pyocr
import pyocr.builders

import cv2
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

    img_path = "/Users/jinnyfruit/PycharmProjects/Openeyes/Backend/static/downloads/test.png"
    wk_builder = pyocr.builders.WordBoxBuilder()
    ocr_results = tool.image_to_string(
        Image.open(img_path),
        lang='kor',
        builder=wk_builder
    )

    img = cv2.imread(img_path)

    editor = []
    before_position = 0
    for ocr_result in ocr_results:
        print(ocr_result.position)
        if ocr_result.position[1][1] - before_position > 30:
            before_position = ocr_result.position[1][1]
            editor.append("\n")
        editor.append(ocr_result.content)
        cv2.rectangle(img, ocr_result.position[0], ocr_result.position[1], (0, 255, 0), 1)

    print("".join(editor).replace(" ", ""))

    cv2.imshow("sample ocr", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()