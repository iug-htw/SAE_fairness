import requests
import os

url = "https://www.neuronpedia.org/api/explanation/search"
api_key = os.getenv("NEURONPEDIA_KEY")
headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key
}

def search_explanations_by_model():
    payload = {
        #Modelle: 
        "modelId": "gemma-2b", 
        #Schichten im Modell?
        "layers": ["0-res-jb", "6-res-jb"],
        "query": "muslim"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())


#search_explanations_by_model()

#Feature runterladen: Featurenummer muss in URL stehen
url = "https://www.neuronpedia.org/api/feature/gpt2-small/0-res-jb/14057"
response = requests.get(url, headers=headers)

print(response.json())
