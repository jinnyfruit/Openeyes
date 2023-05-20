import re
from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank
from transformers import pipeline
import json


# 한국어 추출요약
class OktTokenizer:
    okt: Okt = Okt()
    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens

def Korean_Summerization(text_input) :
    # 1. init using Okt tokenizer
    mytokenizer: OktTokenizer = OktTokenizer()
    lexrank: LexRank = LexRank(mytokenizer)
    text = text_input
    # 2. summarize (like, pre-computation)
    lexrank.summarize(text)

    summerization = []

    # 3. probe (like, query-time)
    summaries: List[str] = lexrank.probe()
    for summary in summaries:
        summerization.append(summary)

    return summerization

def summarize_english_text(text):
    # Load the summarization pipeline with the desired model
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    # Use the pipeline to generate the summary
    summary_dump = summarizer(text, max_length=150, min_length=30, do_sample=False)

    # Print the summarized text
    summary = (summary_dump[0]['summary_text'])

    return summary

def summarize_text(text):
    # Determine language of text
    lang = "en" if re.match(r"^[A-Za-z0-9\s\.,\?]+$", text) else "ko"

    # Summarize English text
    if lang == "en":
        summary = summarize_english_text(text)
    # Summarize Korean text
    else:
        summary = Korean_Summerization(text)
        summary = ' '.join(summary)

    return summary


K_test = "한국은 동아시아에 위치한 반도 국가로, 역사적으로는 고려와 조선 등 다양한 왕조를 거쳐왔습니다. 지리적 특성으로 인해 주변 국가들과의 교류가 활발했으며, 중국의 문화와 영향을 많이 받았습니다. 한글은 15세기에 창제된 한국어의 고유한 문자체계로, 현대 한국어의 표기에 사용되고 있습니다. 한국은 특히 음식 문화로 유명하여, 김치, 불고기, 비빔밥, 떡볶이 등 다양한 음식을 즐기며 특색 있는 맛과 조화로운 조리법으로 인정받고 있습니다. 한국은 또한 한류 문화인 K-pop과 드라마를 통해 글로벌한 인기를 얻고 있으며, 한국의 음악, 연기, 패션 등이 전 세계적으로 사랑받고 있습니다."
E_test = "South Korea, officially known as the Republic of Korea, is a country located in East Asia. With a rich history spanning back thousands of years, it has witnessed the rise and fall of various dynasties. The Korean Peninsula's geographical location has fostered close interactions with neighboring countries, particularly China, influencing its culture and traditions. Korean cuisine is renowned worldwide, with dishes like kimchi, bulgogi, and bibimbap gaining international popularity. South Korea has also made a significant impact through its entertainment industry, known as the Korean Wave or Hallyu, which includes K-pop music, K-dramas, and Korean films. With its unique blend of tradition and modernity, South Korea continues to captivate global audiences with its vibrant culture and technological advancements."

summary = summarize_text(K_test)
print(summary)

# # Sample English text
# english_text = "The quick brown fox jumps over the lazy dog. This sentence is an example of English text that we want to summarize."
# english_summary = summarize_text(english_text)
# print("English text:")
# print(english_text)
# print("Summary:")
# print(english_summary)
# print()
#
# # Sample Korean text
# korean_text = "대한한국의 수도는 서울입니다. 대한민국의 언어는 한국어입니다. 이 문장은 한국어 예시입니다. "
# korean_summary = summarize_text(korean_text)
# print("Korean text:")
# print(korean_text)
# print("Summary:")
# print(korean_summary)
# summary_str = ' '.join(korean_summary)
# print(summary_str)




