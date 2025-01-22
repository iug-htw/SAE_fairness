import requests
import os
import json
# nächster Schritt ist dass die unterschiedliche JSON Struktur der Modelle berücksichtigt wird
#funktioniert für gpt2smk-kk aber nicht für llama3-8b-it-res-jh 
#dort gibt es weitere Hierarchieebene für "neurons"

# Define model and sourceSet tuples
model_source_sets = [
    #("gpt2-small", "res-jb"),fertig
    #("gpt2-small", "att-kk"), fertig
    #weiter!("gpt2-small", "att_32k-oai"),
    #weiter!("gpt2-small", "mlp_32k-oai"),
    #("gemma-2-2b", "gemmascope-att-16k"),kurze Liste fertig
    #("gemma-2-2b", "gemmascope-att-65k"),kurze Liste fertig
    ("gemma-2-2b", "gemmascope-mlp-16k"),kurze Liste fertig
    #("gemma-2-2b", "gemmascope-mlp-65k"), überspringen!
    #("gemma-2-2b", "gemmascope-res-16k"), überspringen!
    #("gemma-2-2b", "gemmascope-res-65k"), überspringen!
    #("gemma-2-9b", "gemmascope-res-16k"), überspringen!
    #("gemma-2-9b-it", "gemmascope-res-16k"), überspringen!
    #("gemma-2-9b-it", "gemmascope-res-131k"),  
    #("llama3.1-8b","llamascope-res-32k"),
]

api_key = os.getenv("NEURONPEDIA_KEY")

#prior queries not included anymore: see queries.json
queries = [
    #"muslim",
    #"islam",
    #"burka",
    #"juif",
    #"kosher",
    #"lady",
    #"shabbat",
    #"programmer",
    #"muslim",
    "woman",
    "christian",
    "money",
    "boy",
    "christianity",
    "Oma",
    "allah",
    "nurse",
    "Mann",
    "man",
    "baptsim",
    "bible",
    "islam",
    "halal",
    "fundamentalist",
    "jesus",
    "gospel",
    "male",
    "temple",
    "professor",
    "receptionist",
    "Jude",
    "jew",
    "she",
    "Frau",
    "sacrament",
    "son",
    "judaism",
    "midwife",
    "he",
    "church",
    "kippah",
    "grandma",
    "grandpa",
    "daughter",
    "homophob",
    "girl",
    "talmud",
    "engineer",
    "terrorist",
    "cocaine",
    "mosque",
    "mecca",
    "nose",
    "Opa",
    "boss",
    "firefighter",
    "doctor",
    "hijab",
    "torah",
    "Junge",
    "wife",
    "quran",
    "synagogue",
    "assistant",
    "queen",
    "gentleman",
    "pope",
    "homemaker",
    "M\u00e4dchen",
    "husband",
    "female",
    "king",
    "naive"
    ] # Query to search for

headers = {
   "Content-Type": "application/json",
   "X-Api-Key": "YOUR_SECRET_TOKEN"#api_key
}

def load_existing_queries(filename='queries3.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_queries(queries, filename='queries3.json'):
    with open(filename, 'w') as file:
        json.dump(queries, file, indent=4)

def search_latent_features_by_model(query, model, source_set): 
    # https://www.neuronpedia.org/api-doc#tag/search
    url = "https://www.neuronpedia.org/api/search-all"

    data = {
        "modelId": model,  # Replace with your desired modelId
        "sourceSet": source_set,     # Required SAE set
        "text": query,     # Replace with your input text
        "selectedLayers": [],  # Specify selected layers
        "sortIndexes": [1],        # Sorting tokens
        "ignoreBos": False,        # Whether to ignore BOS token
        "densityThreshold": -1,    # Density threshold
        "numResults": 20           # Maximum number of results
    }   
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    # Print the response data for debugging
    #print("Response Data:", response_data)
    
    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json4/' + model + '/' + source_set + '/'+ query):
        os.makedirs('json4/' + model + '/'+ source_set + '/' + query)  
    
    # Save the JSON response to a file in the 'json' folder
    filename = 'json4/' + model + '/'+ source_set + '/' + query + '/explanation_for_query_' + query + '.json'
    with open(filename, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    
    # Extract the featureId from the response
    features = []
    for result in response_data['result']:
        model = result['modelId']
        source_set = source_set
        layer = result.get('layer')
        index = result.get('index')
        features.append((model, source_set, layer, index))
    
    return features

def search_explanations_by_feature(feature,query):
    #get Feature aus API https://www.neuronpedia.org/api-doc#tag/features/GET/api/feature/{modelId}/{layer}/{index}
    #Featurenummer muss in URL stehen
    model, source_set, layer, index = feature
    print("model: ", model)
    url = "https://www.neuronpedia.org/api/feature/"+model+'/'+str(layer)+"/"+ str(index)
    print(url)
    response = requests.get(url, headers=headers)
    
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = 'json4/'+model+'/'+ source_set + '/'+query+'/data_for_feature_' + str(index) + '.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Data saved to {filename}")
    #print(response.json())



# Main execution
for model, source_set in model_source_sets:
    for query in queries:
        print(f"Processing query '{query}' for model '{model}' with source set '{source_set}'")
        features = search_latent_features_by_model(query, model, source_set)  # Search explanations by model
        #print("Features found: ", features)  # Print the features found
        if features:
            for feature in features:
                print("Feature: ", feature)
                search_explanations_by_feature(feature, query)
        else:
            print("Feature IDs not found in the response.")

# Save the updated list of all queries
existing_queries = load_existing_queries()
all_queries = list(set(existing_queries + queries))  # Combine and remove duplicates
save_queries(all_queries)