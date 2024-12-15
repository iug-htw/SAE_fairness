import requests
import os
import json


api_key = os.getenv("NEURONPEDIA_KEY")
modelId = "gpt2-small" 
#prior queries not included anymore: islam, muslim, "terrorist","christian","christianity
queries = ["terrorist","christian","christianity"] # Query to search for

headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key
}

def search_latent_features_by_model(query):
    #search by model aus API https://www.neuronpedia.org/api-doc#tag/explanations/POST/api/explanation/search-model
    url = "https://www.neuronpedia.org/api/explanation/search-model"

    payload = {
        "modelId": modelId,
        "query": query,
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json/'+query):
        os.makedirs('json/'+query)  
    # Save the JSON response to a file in the 'json' folder
    filename = 'json/'+query+'/explanation_for_query_'+query+'.json'
    with open(filename, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    # Extract the featureId from the response
    features = []
    for result in response_data.get('results', []):
        layer = result.get('layer')
        index = result.get('index')
        features.append((layer, index))
    print(features)
    return features


def search_explanations_by_feature(feature,query, modelID=modelId):
    #get Feature aus API https://www.neuronpedia.org/api-doc#tag/features/GET/api/feature/{modelId}/{layer}/{index}
    #Featurenummer muss in URL stehen
    layer, index = feature
    
    url = "https://www.neuronpedia.org/api/feature/"+modelID+"/"+str(layer)+"/"+ str(index)
    print(url)
    response = requests.get(url, headers=headers)
    
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = 'json/'+query+'/data_for_feature_' + str(index) + '.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Data saved to {filename}")
    #print(response.json())



# Main execution
for query in queries:
    features = search_latent_features_by_model(query)  # Search explanations by model
    print(features)
    output_filename = 'json/'+query+'/all_output_data_'+str(query)+'.json'
    if features:
        for feature in features:
            search_explanations_by_feature(feature,query,modelId)
    else:
        print("Feature IDs not found in the response.")

