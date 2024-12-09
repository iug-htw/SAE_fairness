import requests
import os
import json

url = "https://www.neuronpedia.org/api/explanation/search"
api_key = os.getenv("NEURONPEDIA_KEY")
headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key
}

def search_explanations_by_model():
    query = "muslim"
    payload = {
        #Modelle: 
        "modelId": "gemma-2b", 
        #Schichten im Modell?
        "layers": ["0-res-jb", "6-res-jb"],
        "query": query,
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json'):
        os.makedirs('json')
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = 'json/explanation_for_query_'+query+'.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)



search_explanations_by_model()

def search_explanations_by_feature():
    #Featurenummer muss in URL stehen
    featureId= str(14057)
    url = "https://www.neuronpedia.org/api/feature/gpt2-small/0-res-jb/" + featureId
    response = requests.get(url, headers=headers)
    print(response.json())
    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json'):
        os.makedirs('json')
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = 'json/data_for_feature_' + featureId + '.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(response.json())

search_explanations_by_feature()