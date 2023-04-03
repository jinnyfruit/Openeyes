import openai
import re
from konlpy.tag import Komoran


# Load API key from file
with open("openai_key.txt", "r") as f:
    api_key = f.read().strip()

# Set up OpenAI API client
openai.api_key = api_key

# Define function to preprocess Korean text
def preprocess_korean_text(text):
    # Use Komoran tokenizer to split text into morphemes
    komoran = Komoran()
    morphemes = komoran.pos(text)

    # Keep only nouns, adjectives, and verbs
    filtered_morphemes = [morph for morph in morphemes if morph[1] in ["NNG", "NNP", "VA", "VV"]]

    # Reconstruct filtered text
    filtered_text = "".join([morph[0] for morph in filtered_morphemes])

    return filtered_text

# Define function to summarize text
def summarize_text(text):
    # Determine language of text
    lang = "en" if re.match(r"^[A-Za-z0-9\s\.,\?]+$", text) else "ko"

    # Preprocess Korean text
    if lang == "ko":
        text = preprocess_korean_text(text)

    # Generate summary using OpenAI's GPT-3 model
    prompt = f"Please summarize the following {lang} text in a concise way:\n\n{text}\n\nSummary:"
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

# Sample English text
english_text = "The quick brown fox jumps over the lazy dog. This sentence is an example of English text that we want to summarize."
english_summary = summarize_text(english_text)
print("English text:")
print(english_text)
print("Summary:")
print(english_summary)
print()

# Sample Korean text
korean_text = "한국의 수도는 서울입니다. 대한민국의 언어는 한국어입니다. 이 문장은 한국어 예시입니다."
korean_summary = summarize_text(korean_text)
print("Korean text:")
print(korean_text)
print("Summary:")
print(korean_summary)