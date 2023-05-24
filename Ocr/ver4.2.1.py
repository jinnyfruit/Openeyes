import pytesseract
import re
from PIL import Image
import os
import openai

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# TESSDATA_PREFIX 환경 변수 설정
os.environ["TESSDATA_PREFIX"] = r"/Users/jinnyfruit/Desktop/tessdata"

# OpenAI ChatGPT 설정
openai.api_key = "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"
engine = "text-davinci-003"

def ocr_image(image_path, lang):
    image = Image.open(image_path)
    ocr_result = pytesseract.image_to_string(image, lang=lang)
    return ocr_result

def get_language(Kor_ocr_result, Eng_ocr_result, form):
    # ChatGPT에게 언어학적으로 맞는 답을 물어보기
    response = openai.Completion.create(
        engine=engine,
        prompt=form,
        temperature=0.3,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0
    )

    # ChatGPT의 답변에서 언어 추출
    text = response.choices[0].text.strip().lower()
    return text

def extract_language(text):
    # 정규표현식을 사용하여 "korean" 또는 "english" 단어 추출
    pattern = r"\b(korean|english)\b"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    extracted_words = [word.lower() for word in matches]

    return extracted_words

def list_to_string(lst):
    # 리스트의 요소들을 문자열로 변환하여 연결
    result = ' '.join(map(str, lst))
    return result

# 이미지 파일 경로
image_path = "/Users/jinnyfruit/PycharmProjects/Openeyes/Backend/static/downloads/test3.png"

# 한국어 OCR 수행
result_kor = ocr_image(image_path, lang="kor")
print("한국어 OCR 결과:")
print(result_kor)

# 영어 OCR 수행
result_eng = ocr_image(image_path, lang="eng")
print("영어 OCR 결과:")
print(result_eng)

# 한글 또는 영어로 변환
# result_kor = "".join(result_kor.split())
# result_eng = "".join(result_eng.split())
result_kor = " ".join(result_kor.split())
result_kor = result_kor.replace("\n", " ")
result_eng = " ".join(result_eng.split())
result_eng = result_eng.replace("\n", " ")


# ChatGPT Regex Prompt format
form= f"If you think Korean is linguistically correct between the two texts, print out the word Korean, and if you think English is correct, print out English. Only one language must be printed out, Korean or English.\n\n Korean-text:{result_kor} English-text:{result_eng}"
print(form)

lang = get_language(result_kor, result_eng, form)
print("\n---------chatGPT result---------")
print(lang)

# "korean" 또는 "english" 단어 추출
extracted_lang = extract_language(lang)
extracted_lang = list_to_string(extracted_lang)

print("--------language--------")
print(extracted_lang)

if extracted_lang == "kor":
    print("-----This text is Korean-----")
    print(result_kor)

elif extracted_lang == "eng":
    print("-----This text is English-----")
    print(result_eng)


