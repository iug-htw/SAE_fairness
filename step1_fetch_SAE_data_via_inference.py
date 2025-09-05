"""
step1_fetch_SAE_data_via_inference.py

This script implements Step 1 of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose:
--------
Fetch latent feature activations from Sparse Autoencoders (SAEs) via the Neuronpedia API 
for a curated set of religion- and violence-related queries.

Workflow:
---------
1. Iterate over all (model, SAE) source set pairs.
2. For each query string, call the Neuronpedia API to retrieve the top-k (default: 20) latent features.
3. Save the results (feature metadata + activation texts) as JSON files to a structured directory.

Notes:
------
This script only handles *data collection* (RQ1/RQ2 setup).
Subsequent analysis (feature overlap, semantic probing) is performed in later steps.
"""

import requests
import os
import json


# API key for authentication (must be set as environment variable)
api_key = os.getenv("NEURONPEDIA_KEY")

headers = {
   "Content-Type": "application/json",
   "X-Api-Key": api_key # api_key
}

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def load_existing_queries(filename='queries5.json'):
    """ Load previously saved queries from a JSON file. """

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
        
    return []

def save_queries(queries, filename='queries5.json'):
    """ Save queries to a JSON file. """

    with open(filename, 'w') as file:
        json.dump(queries, file, indent=4)

def search_latent_features_by_model(query, model, source_set, base_dir='json7'): 
    """
    Query Neuronpedia for top latent features activated by a given text input.

    Parameters
    ----------
    query : str
        Input text (religion/violence-related sentence).
    model : str
        Model identifier (e.g., 'gemma-2-9b').
    source_set : str
        SAE source set identifier (e.g., 'gemmascope-res-16k').
    base_dir : str
        Root directory for saving results.

    Returns
    -------
    list of tuples
        List of features (model, source_set, layer, index).
    """

    url = "https://www.neuronpedia.org/api/search-all"

    # Payload for API request
    data = {
        "modelId": model,
        "sourceSet": source_set,   
        "text": query,   
        "selectedLayers": [],
        "sortIndexes": [],      
        "ignoreBos": True,      
        "densityThreshold": 0.01,  
        "numResults": 20         
    }   
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
        
    # Create 'json' folder if it doesn't exist
    if not os.path.exists(base_dir + '/' + model + '/' + source_set + '/'+ query):
        os.makedirs(base_dir + '/' + model + '/'+ source_set + '/' + query)  
    
    # Save full API response for traceability
    filename = base_dir + '/' + model + '/'+ source_set + '/' + query + '/explanation_for_query_' + query + '.json'
    with open(filename, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
    
    # Extract relevant features (model, layer, index)
    features = []
    for result in response_data['result']:
        model = result['modelId']
        source_set = source_set
        layer = result.get('layer')
        index = result.get('index')
        features.append((model, source_set, layer, index))
    
    return features

def search_explanations_by_feature(feature, query, base_dir='json7'):
    """
        Retrieve detailed information for a given latent feature from Neuronpedia.

        Parameters
        ----------
        feature : tuple
            (model, source_set, layer, index) identifying the feature.
        query : str
            Original input query string (used for directory structure).
        base_dir : str
            Root directory for saving results.

        Saves
        -----
        JSON file with feature explanation, including activation texts.
    """
        
    model, source_set, layer, index = feature
    print("model: ", model)
    url = "https://www.neuronpedia.org/api/feature/"+model+'/'+str(layer)+"/"+ str(index)
    print(url)
    response = requests.get(url, headers=headers)
    
    # Save the JSON response to a file in the 'json' folder
    json_data = response.json()
    filename = base_dir + '/'+ model + '/' + source_set + '/' +query+ '/data_for_feature_' + str(index) + '.json'

    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Data saved to {filename}")

# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def fetch_SAE_data_via_inference(model_source_sets, queries, base_dir='json7'):
    """
        Fetch SAE activations for all models and queries.

        Parameters
        ----------
        model_source_sets : list of tuples
            List of (model, SAE) pairs to analyze.
        queries : list of str
            Religion/violence queries to probe.
        base_dir : str
            Directory root for saving JSON outputs.

        Process
        -------
        1. For each (model, SAE) pair:
        - Query Neuronpedia with each input string.
        - Retrieve top latent features.
        - Save activation metadata + feature explanations.
    """
        
    # Main execution
    for model, source_set in model_source_sets:
        for query in queries:
            print(f"Processing query '{query}' for model '{model}' with source set '{source_set}'")
            features = search_latent_features_by_model(query, model, source_set, base_dir)  # Search explanations by model

            if features:
                for feature in features:
                    print("Feature: ", feature)
                    search_explanations_by_feature(feature, query, base_dir)
            else:
                print("Feature IDs not found in the response.")


if __name__ == "__main__":
    model_source_sets = [
        ("gpt2-small", "res-jb"),
        ("gpt2-small", "att-kk"),
        ("gemma-2-2b", "gemmascope-att-16k"),
        ("gemma-2-2b", "gemmascope-res-16k"), 
        ("gemma-2-2b", "gemmascope-res-65k"), 
        ("gemma-2-9b", "gemmascope-res-16k"), 
        ("gemma-2-9b-it", "gemmascope-res-16k"), 
        ("gemma-2-9b-it", "gemmascope-res-131k"),  
        ("llama3.1-8b","llamascope-res-32k"),
    ]

    with open('queries7.json', 'r') as file:
        queries = json.load(file)

    fetch_SAE_data_via_inference(model_source_sets, queries)
    print("Data fetching completed.")