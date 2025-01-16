import requests
import os
import json
# nächster Schritt ist dass die unterschiedliche JSON Struktur der Modelle berücksichtigt wird
#funktioniert für gpt2smk-kk aber nicht für llama3-8b-it-res-jh 
#dort gibt es weitere Hierarchieebene für "neurons"


releaseNames = [#"gemma-scope",
                #"gpt2sm-apollojt",
                #"gpt2sm-kk",
                #"gpt2sm-rfs-jb",
                #"llama-scope", 
                #"llama3-8b-it-res-jh",
                #"llama3.1-8b-eleuther_gp",
]
api_key = os.getenv("NEURONPEDIA_KEY")


#prior queries not included anymore: see queries.json
queries = [
    "gospel"       
    ] # Query to search for

headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key
}

def load_existing_queries(filename='queries.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_queries(queries, filename='queries.json'):
    with open(filename, 'w') as file:
        json.dump(queries, file, indent=4)

def search_latent_features_by_model(query,modelID): 
    #search by model aus API https://www.neuronpedia.org/api-doc#tag/explanations/POST/api/explanation/search-model
    url = "https://www.neuronpedia.org/api/explanation/search-release"

    payload = {
        "releaseName": modelID,
        "query": query,
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    response_data = response.json()
    
    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json/'+modelID+'/'+query):
        os.makedirs('json/'+modelID+'/'+query)  
    # Save the JSON response to a file in the 'json' folder
    filename = 'json/'+modelID+'/'+query+'/explanation_for_query_'+query+'.json'
    with open(filename, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    # Extract the featureId from the response
    features = []
    for result in response_data.get('results', []):
        model= result.get('modelId')
        layer = result.get('layer')
        index = result.get('index')
        features.append((model, layer, index))
    print(features)
    return features


def search_explanations_by_feature(feature,query):
    #get Feature aus API https://www.neuronpedia.org/api-doc#tag/features/GET/api/feature/{modelId}/{layer}/{index}
    #Featurenummer muss in URL stehen
    model, layer, index = feature
    
    url = "https://www.neuronpedia.org/api/feature/"+model+'/'+str(layer)+"/"+ str(index)
    print(url)
    response = requests.get(url, headers=headers)
    
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = 'json/'+modelID+'/'+query+'/data_for_feature_' + str(index) + '.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Data saved to {filename}")
    #print(response.json())



# Main execution
for releaseName in releaseNames:
    modelID = releaseName
    for query in queries:
        features = search_latent_features_by_model(query,modelID)  # Search explanations by model
        print(features) #die Features werden hier das 2. mal ausgegeben
        if features:
            for feature in features:
                search_explanations_by_feature(feature,query)
        else:
            print("Feature IDs not found in the response.")

# Save the updated list of all queries
existing_queries = load_existing_queries()
all_queries = list(set(existing_queries + queries))  # Combine and remove duplicates
save_queries(all_queries)