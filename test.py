from typing import List
from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank
import json

#한국어 추출요약
class OktTokenizer:
    okt: Okt = Okt()
    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens

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