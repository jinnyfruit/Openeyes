from typing import List
import re
from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank
import openai
import json
import time


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

# Load API key from file
with open("openai_key.txt", "r") as f:
    api_key = f.read().strip()

# Set up OpenAI API client
openai.api_key = api_key

def summarize_english_text(text):
    # Generate summary using OpenAI's GPT-3 model
    prompt = f"Please summarize the following English text in a concise way:\n\n{text}\n\nSummary:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract summary from API response
    summary = response.choices[0].text.strip()

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

#test_text = "Scientists have discovered a new species of bird in the Amazon rainforest. The bird, which has been named the black-crowned antpitta, has a distinctive black crown on its head and is known for its unique song. The discovery of the black-crowned antpitta is significant because it adds to our understanding of the incredible biodiversity of the Amazon rainfores."
#test_text = "서울시는 자전거 교통 활성화를 위해 자전거 도로 건설에 노력하고 있습니다. 자전거 도로는 차량과 보행자와 구분되어 있어 안전하게 이용할 수 있습니다. 또한 자전거 대여소도 많이 설치하여 더 많은 시민들이 자전거를 이용할 수 있도록 노력하고 있습니다."
test_text = """
The World Health Organization declared COVID-19 a global pandemic on March 11, 2020. Since then, it has had a significant impact on countries, economies, and societies worldwide. The virus, also known as SARS-CoV-2, spreads primarily through respiratory droplets when an infected person coughs, sneezes, or talks.

COVID-19 symptoms vary from mild to severe, and some infected individuals may remain asymptomatic. Common symptoms include fever, cough, fatigue, and shortness of breath. Older adults and people with underlying health conditions are at higher risk of developing severe illness.

To control the spread of the virus, various measures have been implemented, including wearing masks, practicing social distancing, and frequent handwashing. Additionally, vaccines have been developed and rolled out globally, providing protection against COVID-19.

The pandemic has disrupted daily life, leading to changes in work routines, school closures, travel restrictions, and the rise of remote work and virtual events. It has also impacted sectors such as tourism, hospitality, and entertainment.

As the situation evolves, it is crucial to stay informed about the latest developments and follow guidelines provided by health authorities to protect ourselves and others from COVID-19.
"""

# Start the timer
start_time = time.time()

summary = summarize_text(test_text)
print(summary)

# Stop the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
print("\nElapsed Time:", elapsed_time, "seconds")

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


