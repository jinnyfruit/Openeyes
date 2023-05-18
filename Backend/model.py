import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import numpy as np
from collections import Counter
import pyocr
from PIL import Image
from ultralytics import YOLO
import cv2
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

    def modeling(self, mode, path_dlocal, path_ulocal):
        # image open
        try:
            img = Image.open(path_dlocal)
        except:
            self.error = 'please check url of image'
            return

        if mode == "0":
            img = self.object(img)

        elif mode == "1":
            img = self.ocr(img)
            # self.summarize()

        print("== self.info ====")
        print(self.info)

        # store model image
        cv2.imwrite(path_ulocal, img)

        return self.info, self.summary, self.error

    def object(self, img):
        model = YOLO("yolov8n.pt")

        obj_results = model(img, device="mps")
        obj_result = obj_results[0]

        img = np.asarray(img)
        bboxes = np.array(obj_result.boxes.xyxy.cpu(), dtype="int")

        for bbox in bboxes:
            (x, y, x2, y2) = bbox
            cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 225), 2)

        classes = np.array(obj_result.boxes.cls.cpu(), dtype="int")
        class_list = []

        for i in range(len(classes)):
            class_list.append(model.names[classes[i]])

        self.info = dict(Counter(class_list))

        return img

    def ocr(self, img):
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            self.error = "OCR tool is not found"
            return

        tool = tools[0]
        wk_builder = pyocr.builders.WordBoxBuilder()
        ocr_results = tool.image_to_string(
            img,
            lang="kor+eng",
            builder=wk_builder
        )

        img = np.asarray(img)

        editor = []
        before_position = 0
        for ocr_result in ocr_results:
            if ocr_result.position[1][1] - before_position > 30:
                before_position = ocr_result.position[1][1]
                editor.append('\n')
            editor.append(ocr_result.content)
            cv2.rectangle(img, ocr_result.position[0], ocr_result.position[1], (0, 255, 255), 1)

        self.info = editor

        return img

    def summarize(self, text):
        
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
         


# M = Model()
# M.modeling("0", "static/downloads/0_jyeon_IMG_3080.jpg", "static/uploads/1_jyeon_IMG_3080.jpg")
# M.modeling("1", "static/downloads/1_jyeon_IMG0515.png", "static/uploads/1_jyeon_IMG0515.png")
