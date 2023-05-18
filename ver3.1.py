from transformers import pipeline

# Load the summarization pipeline with the desired model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Define the text you want to summarize
text = """
The World Health Organization declared COVID-19 a global pandemic on March 11, 2020. Since then, it has had a significant impact on countries, economies, and societies worldwide. The virus, also known as SARS-CoV-2, spreads primarily through respiratory droplets when an infected person coughs, sneezes, or talks.

COVID-19 symptoms vary from mild to severe, and some infected individuals may remain asymptomatic. Common symptoms include fever, cough, fatigue, and shortness of breath. Older adults and people with underlying health conditions are at higher risk of developing severe illness.

To control the spread of the virus, various measures have been implemented, including wearing masks, practicing social distancing, and frequent handwashing. Additionally, vaccines have been developed and rolled out globally, providing protection against COVID-19.

The pandemic has disrupted daily life, leading to changes in work routines, school closures, travel restrictions, and the rise of remote work and virtual events. It has also impacted sectors such as tourism, hospitality, and entertainment.

As the situation evolves, it is crucial to stay informed about the latest developments and follow guidelines provided by health authorities to protect ourselves and others from COVID-19.
"""

# Use the pipeline to generate the summary
summary = summarizer(text, max_length=150, min_length=30, do_sample=False)

# Print the summarized text
print(summary[0]['summary_text'])
