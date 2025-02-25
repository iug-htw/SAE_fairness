import requests
import os
import json
# nächster Schritt ist dass die unterschiedliche JSON Struktur der Modelle berücksichtigt wird
#funktioniert für gpt2smk-kk aber nicht für llama3-8b-it-res-jh 
#dort gibt es weitere Hierarchieebene für "neurons"

# Define model and sourceSet tuples
model_source_sets = [
    ("gpt2-small", "res-jb"),# fertig
    ("gpt2-small", "att-kk"), #fertig
    #("gpt2-small", "att_32k-oai"), ging nicht
    #("gpt2-small", "mlp_32k-oai"),übersprungen
    ("gemma-2-2b", "gemmascope-att-16k"), #fertig
    #("gemma-2-2b", "gemmascope-att-65k"), geht nicht
    #("gemma-2-2b", "gemmascope-mlp-16k"), geht nicht
    #("gemma-2-2b", "gemmascope-mlp-65k"),  geht nicht
    ("gemma-2-2b", "gemmascope-res-16k"), # fertig
    ("gemma-2-2b", "gemmascope-res-65k"), #   fertig
    ("gemma-2-9b", "gemmascope-res-16k"), #   fertig
    ("gemma-2-9b-it", "gemmascope-res-16k"), #  fertig
    ("gemma-2-9b-it", "gemmascope-res-131k"),  #  fertig
    ("llama3.1-8b","llamascope-res-32k"),
]

api_key = os.getenv("NEURONPEDIA_KEY")

#for data collection in education sortIndexes is empty (no token number) --> searches by max activation of phrase

#prior queries not included anymore: see queries.json
queries = [
  "This is naive",
  "This is money",
  "This is a terrorist",
  "This is an attack",
  "This is a victim"
    # "I learn calculus",
    # "I learn algebra",
    # "I learn geometry",
    # "I learn trigonometry",
    # "I learn statistics",
    # "I learn probability",
    # "I learn physics",
    # "I learn chemistry",
    # "I learn biology",
    # "I learn astronomy",
    # "I learn geology",
    # "I learn geography",
    # "I learn programming",
    # "I learn computer science",
    # "I learn history",
    # "I learn economics",
    # "I learn politics",
    # "I learn psychology",
    # "I learn sociology",
    # "I learn anthropology",
    # "I learn philosophy",
    # "I learn literature",
    # "I learn poetry",
    # "I learn music",
    # "I learn art",
    # "I learn dance",
    # "I learn theater",
    # "I learn film",
    # "I teach calculus",
    # "I teach algebra",
    # "I teach geometry",
    # "I teach trigonometry",
    # "I teach statistics",
    # "I teach probability",
    # "I teach physics",
    # "I teach chemistry",
    # "I teach biology",
    # "I teach astronomy",
    # "I teach geology",
    # "I teach geography",
    # "I teach programming",
    # "I teach computer science",
    # "I teach history",
    # "I teach economics",
    # "I teach politics",
    # "I teach psychology",
    # "I teach sociology",
    # "I teach anthropology",
    # "I teach philosophy",
    # "I teach literature",
    # "I teach poetry",
    # "I teach music",
    # "I teach art",
    # "I teach dance",
    # "I teach theater",
    # "I teach film",
    # "I study calculus",
    # "I study algebra",
    # "I study geometry",
    # "I study trigonometry",
    # "I study statistics",
    # "I study probability",
    # "I study physics",
    # "I study chemistry",
    # "I study biology",
    # "I study astronomy",
    # "I study geology",
    # "I study geography",
    # "I study programming",
    # "I study computer science",
    # "I study history",
    # "I study economics",
    # "I study politics",
    # "I study psychology",
    # "I study sociology",
    # "I study anthropology",
    # "I study philosophy",
    # "I study literature",
    # "I study poetry",
    # "I study music",
    # "I study art",
    # "I study dance",
    # "I study theater",
    # "I study film",

    #"This is a muslim",
    #"This is a burka",
    #"This is a lady",
    #"This is a programmer",
    #"This is a woman",
    #"This is a christian",
    #"This is a boy",
    #"This is a nurse",
    #"This is a man",
    #"This is a baptsim",
    #"This is a bible",
    #"This is a fundamentalist",
    #"This is a gospel",
    #"This is a male",
    #"This is a temple",
    #"This is a professor",
    #"This is a receptionist",
    #"This is a jew",
    #"This is a sacrament",
    #"This is a son",
    #"This is a midwife",
    #"This is a church",
    #"This is a kippah",
    #"This is a grandma",
    #"This is a grandpa",
    #"This is a daughter",
    #"This is a homophob",
    #"This is a girl",
    #"This is a talmud",
    #"This is an engineer",
    #"This is a terrorist",
    #"Das ist ein Jude",
    #"Das ist eine Frau",
    #"This is a mosque",
    #"Das ist ein Opa",
    #"This is a boss",
    #"This is a firefighter",
    #"This is a doctor",
    #"This is a hijab",
    #"This is a torah",
    #"Das ists ein Junge",
    #"This is a wife",
    #"This is a quran",
    #"This is a synagogue",
    #"This is an assistant",
    #"This is a queen",
    #"This is a gentleman",
    #"This is a pope",
    #"This is a homemaker",
    #"Das ist ein M\u00e4dchen",
    #"This is a husband",
    #"This is a king",
    #"Das ist ein Mann",
    #"Das ist eine Oma",
    #"This is islam", # change to 3rd token from here
    #"This is he",
    #"This is christianity",
    #"This is jesus",
    #"This is she",
    #"This is judaism",
    #"This is cocaine",
    #"This is mecca",
    #"this is nose",
    #"this is female",
    #"This is naive"
    #"This is money",
    #"This is shabbat",
    #"il est juif",
    #"This is kosher",
    #"This is allah",
    #"This is halal",
    ] # Query to search for

headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key#api_key
}

def load_existing_queries(filename='queries5.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_queries(queries, filename='queries5.json'):
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
        "sortIndexes": [],        # Sorting tokens
        "ignoreBos": True,        # Whether to ignore BOS token
        "densityThreshold": 0.01,    # Density threshold as on website
        "numResults": 20           # Maximum number of results
    }   
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    # Print the response data for debugging
    #print("Response Data:", response_data)
    
    # Create 'json' folder if it doesn't exist
    if not os.path.exists('json5/' + model + '/' + source_set + '/'+ query):
        os.makedirs('json5/' + model + '/'+ source_set + '/' + query)  
    
    # Save the JSON response to a file in the 'json' folder
    filename = 'json5/' + model + '/'+ source_set + '/' + query + '/explanation_for_query_' + query + '.json'
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
    filename = 'json5/'+model+'/'+ source_set + '/'+query+'/data_for_feature_' + str(index) + '.json'
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