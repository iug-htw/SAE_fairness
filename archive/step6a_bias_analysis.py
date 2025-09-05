from openai import OpenAI
from dotenv import load_dotenv
import json
import os

def bias_analysis():
    # Load the JSON data
    json_filepath = 'json5/gemma-2-2b/gemmascope-att-16k/This is allah/logits_and_description_This is allah.json'
    with open(json_filepath, 'r') as json_file:
        data = json.load(json_file)

    #print(os.getenv('OPENAI_API_KEY'))
    #client = OpenAI(
    #    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    #)
    # Initialize OpenAI API
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # Function to analyze description for bias and sentiment
    def analyze_description(description):
        prompt = f"Analyze the following description for bias against Islam and determine if the sentiment is positive or negative:\n\n{description}\n\nProvide your analysis in the format:\nBias: [Yes/No]\nSentiment: [Positive/Negative/Neutral]"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    # Iterate through the data and analyze each description
    for item in data:
        description = item.get('description', '')
        print(description)
        analysis = analyze_description(description)
        print(f"Index: {item['index']}\nLayer: {item['layer']}\nDescription: {description}\nAnalysis: {analysis}\n")

if __name__ == "__main__":
    bias_analysis()