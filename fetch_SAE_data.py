import requests
import os

url = "https://www.neuronpedia.org/api/explanation/search"

payload = {
    "modelId": "gemma-2b",
    "layers": ["0-res-jb", "6-res-jb"],
    "query": "muslim woman"
}
api_key = os.getenv("NEURONPEDIA_KEY")
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": api_key
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())