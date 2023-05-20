import openai
import re
from konlpy.tag import Komoran
from lexrankr import LexRank

def Summerization() :
    # 1. init using Okt tokenizer
    mytokenizer: OktTokenizer = OktTokenizer()
    lexrank: LexRank = LexRank(mytokenizer)
    text = "코로나 팬데믹 시대, 디지털 기술은 교육의 생명선이 됐다. OECD 설문조사 결과, 지난 1년 간 교사와 학생들은 온라인 학습에 빠르게 적응했다. 대부분 국가들은 디지털 학습 기회를 빠르게 제공하고, 교사들의 협업을 장려했다. 특히 중등 교육에서 국가 전반에 걸쳐 온라인 플랫폼이 광범위하게 사용됐다. OECD 회원국은 교육 시스템을 원격 또는 블렌디드 학습으로 전환했다. 이는 특히 교사에게 많은 책임을 부여했다. 교사들은 가상 학습 환경에 적합한 자료를 준비하는 한편 ‘학생들을 위한 디지털 기기 지원 및 자원 조정’, ‘학부모와의 상호 작용’ 등 새로운 임무를 맡게 됐다.  "

    # 2. summarize (like, pre-computation)
    lexrank.summarize(text)

    summerization = []

    # 3. probe (like, query-time)
    summaries: List[str] = lexrank.probe()
    for summary in summaries:
        summerization.append(summary)

    return summerization

result = Summerization()

print(result)

# Load API key from file
with open("openai_key.txt", "r") as f:
    api_key = f.read().strip()

# Set up OpenAI API client
openai.api_key = api_key

# Define function to summarize English text
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

# Define function to determine language and summarize text
def summarize_text(text):
    # Determine language of text
    lang = "en" if re.match(r"^[A-Za-z0-9\s\.,\?]+$", text) else "ko"

    # Summarize English text
    if lang == "en":
        summary = summarize_english_text(text)
    # Summarize Korean text
    else:
        summary = summarize_english_text(text)

    return summary

# Sample English text
english_text = "The quick brown fox jumps over the lazy dog. This sentence is an example of English text that we want to summarize."
english_summary = summarize_text(english_text)
print("English text:")
print(english_text)
print("Summary:")
print(english_summary)
print()

# Sample Korean text
korean_text = "대한한국의 수도는 서울입니다. 대한민국의 언어는 한국어입니다. 이 문장은 한국어 예시입니다. "
korean_summary = summarize_text(korean_text)
print("Korean text:")
print(korean_text)
print("Summary:")
print(korean_summary)
