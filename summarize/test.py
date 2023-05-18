import re
from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank
from transformers import pipeline


class OktTokenizer:
    okt: Okt = Okt()

    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens


class Model():
    def __init__(self):
        self.info = ""
        self.summary = ""
        self.error = ""

    def summarize(self, text):

        def Korean_Summerization(text_input):
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


text = "서울시는 자전거 교통 활성화를 위해 자전거 도로 건설에 노력하고 있습니다. 자전거 도로는 차량과 보행자와 구분되어 있어 안전하게 이용할 수 있습니다. 또한 자전거 대여소도 많이 설치하여 더 많은 시민들이 자전거를 이용할 수 있도록 노력하고 있습니다."

M = Model()
print(M.summarize(text))
