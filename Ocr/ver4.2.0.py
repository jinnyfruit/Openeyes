import pytesseract
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
form = f"Please look at the two texts and print out only one of the two words, Korean or English, except for all the other words. Don't print out values except for the words Korean or English.\n\n Korean:{result_kor} English:{result_eng}"
print(form)

lang = get_language(result_kor, result_eng, form)
print("\n---------chatGPT result---------")
print(lang)


if lang == "kor":
    print("-----This text is Korean-----")
    print(result_kor)

elif lang == "eng":
    print("-----This text is English-----")
    print(result_eng)


