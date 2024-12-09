import requests
import os
import json


api_key = os.getenv("NEURONPEDIA_KEY")
modelId = "gpt2-small" 


headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key
}

def search_explanations_by_model():
    #search by model aus API https://www.neuronpedia.org/api-doc#tag/explanations/POST/api/explanation/search-model
    url = "https://www.neuronpedia.org/api/explanation/search-model"
    query = "muslim"
    payload = {
        "modelId": modelId,
        "query": query,
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    

    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json'):
        os.makedirs('json')
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = 'json/explanation_for_query_'+query+'.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    # Extract the featureId from the response
    featureIds = []
    for result in response_data.get('results', []):
        features = result.get('index')
        featureIds.append(features)
    return featureIds



def search_explanations_by_feature(featureId,modelID=modelId):
    #get Feature aus API https://www.neuronpedia.org/api-doc#tag/features/GET/api/feature/{modelId}/{layer}/{index}
    #Featurenummer muss in URL stehen
    #featureId= str(14057)
    url = "https://www.neuronpedia.org/api/feature/"+modelID+"/"+'0-res-jb'+"/"+ featureId
    print(url)
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
    #print(response.json())

#search_explanations_by_model()
#search_explanations_by_feature()

# Main execution
featureIds = search_explanations_by_model()
print(featureIds)
if featureIds:
    for featureId in featureIds:
        search_explanations_by_feature(str(featureId),modelId)
else:
    print("Feature IDs not found in the response.")