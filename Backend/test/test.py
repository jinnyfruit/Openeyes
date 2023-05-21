import pytesseract
from pytesseract import Output
import os

# 한국어 언어 지정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
custom_config = r'--oem 3 --psm 6 -l kor'

# TESSDATA_PREFIX 환경 변수 설정
os.environ["TESSDATA_PREFIX"] = r"/Users/jinnyfruit/Downloads/tesseract-ocr-w64-setup-v5.2.0.20220712/肕/tessdata"

# 이미지에서 텍스트 추출
image_path = "/Users/jinnyfruit/PycharmProjects/Openeyes/Backend/static/downloads/test3.png"
result = pytesseract.image_to_string(image_path, lang="kor")


print(result)