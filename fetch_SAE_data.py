import requests
import os
import json


api_key = os.getenv("NEURONPEDIA_KEY")
modelId = "gpt2-small" 
query = "muslim"

headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key
}

def search_latent_features_by_model(query=query):
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


def search_explanations_by_feature(feature,modelID=modelId,query=query):
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
    #print(response.json())

def extract_logits(feature,query=query):
    layer, index = feature
    filename = 'json/'+query+'/data_for_feature_' + str(index) + '.json'
    # Load the JSON data from a file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract the neg_str and pos_str values
    neg_str = data.get('neg_str', [])
    pos_str = data.get('pos_str', [])

    # Extract the layer and description from the explanations
    explanations = data.get('explanations', [])
    if explanations:
        layer = explanations[0].get('layer')
        description = explanations[0].get('description')
    else:
        print("No explanations found.")
    
    # Structure the output data
    output_data = {
        "index": index,
        "layer": layer,
        "url": filename,
        "negative_strings": neg_str,
        "positive_strings": pos_str,
        "description": description
    }
    
    # Save the output data to a JSON file
    output_filename2 = f'json/output_{os.path.basename(filename)}'
    with open(output_filename, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

    print(f"Output saved to {output_filename}")
    return output_data

# Main execution
all_output_data = []  # List to collect all output data
features = search_latent_features_by_model(query)  # Search explanations by model
print(features)
output_filename = 'json/'+query+'/all_output_data_'+str(query)+'.json'
if features:
    for feature in features:
        search_explanations_by_feature(feature,modelId,query)
        output_data = extract_logits(feature,query)
        if output_data:
            all_output_data.append(output_data)
        # Save all collected output data to a single JSON file
else:
    print("Feature IDs not found in the response.")
    
with open(output_filename, 'w') as output_file:
    json.dump(all_output_data, output_file, indent=4)
print(f"All output data saved to {output_filename}")    

