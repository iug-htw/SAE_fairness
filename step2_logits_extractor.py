"""
step2_logits_extractor.py

This script implements Step 2 of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
This step parses the JSON files produced in Step 1 (SAE activations via Neuronpedia) 
and extracts structured information about each latent feature, including:

- Positive and negative activation strings
- Feature descriptions
- Layer and index identifiers

The results are saved as cleaned JSON summaries, one per query, 
which can be used for overlap and semantic analysis in subsequent steps.

Workflow
--------
1. Load the list of religion/violence queries.
2. For each model, residual stream, and query:
   - Open the Neuronpedia JSON response file (`explanation_for_query_<query>.json`).
   - Extract latent feature IDs (layer, index).
   - For each feature, load detailed feature JSON and retrieve:
       * positive and negative activation strings
       * description
       * metadata (layer, index, file path)
   - Save both individual feature summaries and a consolidated file 
     (`logits_and_description_<query>.json`) containing all features for that query.

Inputs
------
- modelReleases : list of model names (e.g., "gemma-2-2b", "gpt2-small")
- queries_file  : JSON file containing the curated religion/violence prompts
- main_dir      : directory containing JSON results from Step 1

Outputs
-------
- Per-feature JSON summaries (output_<original_filename>.json)
- Per-query aggregated JSON summaries (logits_and_description_<query>.json)

Notes
-----
This script transitions the pipeline from **raw data collection** (Step 1) 
to **structured data preparation**, enabling feature overlap analysis (RQ1, RQ2).
"""

import json
import os


# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def load_queries(filename):
    """ Load a list of queries from a JSON file. """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []


def extract_logits(feature, modelRelease, residual_stream, query, output_dir='json'):
    """
    Extract structured feature information (logits and description) from a JSON file.

    Parameters
    ----------
    feature : tuple
        (layer, index) identifiers for the latent feature.
    modelRelease : str
        Model identifier (e.g., 'gemma-2-9b').
    residual_stream : str
        SAE source set / residual stream name (e.g., 'gemmascope-res-16k').
    query : str
        The input query string (e.g., 'This is a church').
    output_dir : str, default='json'
        Directory where feature JSONs are stored.

    Returns
    -------
    dict
        Structured feature metadata with fields:
        - index
        - layer
        - url (path to raw JSON)
        - negative_strings
        - positive_strings
        - description
    """

    layer, index = feature
    filename = os.path.join(output_dir, modelRelease, residual_stream, query,
                            f'data_for_feature_{index}.json')

    if not os.path.exists(filename):
        print(f"File {filename} does not exist. Skipping...")
    else:
        with open(filename, 'r') as file:
            data = json.load(file)

        # Extract activation strings
        neg_str = data.get('neg_str', [])
        pos_str = data.get('pos_str', [])

        # Extract the layer and description from the explanations
        explanations = data.get('explanations', [])
        layer = ""
        description = ""
        if explanations:
            layer = explanations[0].get('layer')
            description = explanations[0].get('description')
        else:
            print(f"❗No explanations found. [{modelRelease}-{residual_stream}-{query}]")
        
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
        output_filename2 = os.path.join(output_dir, modelRelease, residual_stream, query, f'output_{os.path.basename(filename)}')
        with open(output_filename2, 'w') as output_file:
            json.dump(output_data, output_file, indent=4)

        # print(f"Output saved to {output_filename2}")
        return output_data

# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def extract_logits_for_all_queries(modelReleases, queries_file='queries.json', main_dir='json'):
    """
    Process all queries for all models and extract logits/feature metadata.

    Parameters
    ----------
    modelReleases : list
        Models to process (e.g., ["gemma-2-2b", "gpt2-small"]).
    queries_file : str
        Path to JSON file containing the queries.
    main_dir : str
        Root directory containing raw JSON outputs from Step 1.

    Workflow
    --------
    - Iterate over each model and residual stream directory.
    - For each query, open the raw Neuronpedia response file 
      (`explanation_for_query_<query>.json`).
    - Extract features (layer, index).
    - Call `extract_logits(...)` to load per-feature details.
    - Save a consolidated JSON file `logits_and_description_<query>.json`
      with all extracted features for that query.
    """

    queries = load_queries(filename=queries_file)

    for modelRelease in modelReleases:
        # Look inside each residual stream folder
        files = os.listdir(os.path.join(main_dir, modelRelease))

        for residual_stream in files:
            for query in queries:
                all_output_data = []  # Collected results per query

                output_filename = os.path.join(main_dir, modelRelease, residual_stream, query,
                                               f'logits_and_description_{query}.json')
                input_filename = os.path.join(main_dir, modelRelease, residual_stream, query,
                                              f'explanation_for_query_{query}.json')

                if not os.path.exists(input_filename):
                    print(f"File {input_filename} does not exist.")
                    continue

                with open(input_filename, 'r') as json_file:
                    response_data = json.load(json_file)

                # Collect feature IDs (layer, index) from raw response
                features = []
                for result in response_data.get('result', []):
                    layer = result.get('layer')
                    index = result.get('index')
                    features.append((layer, index))
                    
                if features:
                    for feature in features:
                        output_data = extract_logits(feature, modelRelease, residual_stream, query, output_dir=main_dir)
                        if output_data:
                            all_output_data.append(output_data)
                        # Save all collected output data to a single JSON file
                else:
                    print("Feature IDs not found in the response.")
                
                with open(output_filename, 'w') as output_file:
                    json.dump(all_output_data, output_file, indent=4)

                print(f"✅ {query} => {modelRelease}-{residual_stream}")


if __name__ == "__main__":
    modelReleases = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]

    extract_logits_for_all_queries(modelReleases, queries_file='queries6.json', main_dir='json6')
