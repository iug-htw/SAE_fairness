import json
import openai
import os

# If you encounter ModuleNotFoundError, install the openai package using:
# pip install openai

# Load the JSON data
json_filepath = 'json/gemma-scope/allah/logits_and_description_allah.json'
with open(json_filepath, 'r') as json_file:
    data = json.load(json_file)

# Initialize OpenAI API
api_key = os.getenv("OpenAI_KEY")
openai.api_key = api_key

# Function to analyze description for bias and sentiment
def analyze_description(description):
    prompt = f"Analyze the following description for bias against Islam and determine if the sentiment is positive or negative:\n\n{description}\n\nProvide your analysis in the format:\nBias: [Yes/No]\nSentiment: [Positive/Negative/Neutral]"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Iterate through the data and analyze each description
for item in data:
    description = item.get('description', '')
    print(description)
    analysis = analyze_description(description)
    print(f"Index: {item['index']}\nLayer: {item['layer']}\nDescription: {description}\nAnalysis: {analysis}\n")


