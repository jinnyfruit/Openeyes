from transformers import BartTokenizer, BartForConditionalGeneration

# Load the tokenizer and model
tokenizer = BartTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6')
model = BartForConditionalGeneration.from_pretrained('sshleifer/distilbart-cnn-12-6')

# Define the text you want to summarize
text = """
Insert your English text here that you want to summarize.
"""

# Tokenize the text
inputs = tokenizer.encode(text, truncation=True, max_length=1024, return_tensors='pt')

# Generate the summary
summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=150, early_stopping=True)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Print the summarized text
print(summary)
