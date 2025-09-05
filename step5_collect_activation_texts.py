"""
step5_collect_activation_texts.py

This script implements Step 5 of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

The script iterates through all subfolders in the "json4" folder, where each subfolder represents a model.
For each model, it creates a CSV file named "activation_analysis.csv" in the respective model's folder.
The script processes all JSON files in the subfolders of each model, extracting activation tokens and
writing them to the CSV file along with the folder name, query term, and latent feature number.

Purpose
-------
Collect the **activation texts** (tokens that fired strongly) for latent features associated with 
specific religion-related query terms.  
The outputs are written into CSV files, organized by religion group.

Workflow
--------
1. Traverse the base folder containing model outputs.
2. For each (model, source) pair:
   - For each religion group (Christianity, Islam, Judaism, Buddhism, Hinduism):
     - Create a CSV file named `activation_analysis_<religion>.csv`.
3. Within each religion group:
   - Iterate through query subfolders (e.g., "This is a church").
   - Match query terms to the predefined religion-specific term list.
   - For each JSON file (feature explanation) in the subfolder:
     - Extract latent feature number from filename.
     - Read activation tokens from the file.
     - Write `[term, feature_number, tokens]` rows to the CSV.

Inputs
------
- base_folder : str
    Root folder containing per-model and per-source outputs (default: "json5/").

Outputs
-------
- For each (model, source, religion):
  CSV file named `activation_analysis_<religion>.csv` with columns:
    query_term | latent_feature_number | activation_tokens
    
Notes
-----
- This step is **semantic probing**: extracting the actual tokens associated with features, 
  to later analyze whether violence- or geography-related terms appear disproportionately.
"""

import json
import csv
import os

# Define the base folder containing the model subfolders
base_folder = 'json5/'

# Define the CSV file columns
csv_columns = ['query_term', 'latent_feature_number', 'activation_tokens']

# Define the query terms to be used, grouped by religion
query_terms_sets = {
    'christianity': ["baptism", "bible", "christian", "church", "gospel", "pope", "sacrament", "christianity", "jesus", "priest", "pastor", "crucifix", "communion",],
    'islam': ["burka", "hijab", "mosque", "muslim", "quran", "allah", "halal", "islam", "mecca", "imam", "ramadan", "eid", "hajj",],
    'judaism': ["jew", "kippah", "synagogue", "talmud", "torah", "judaism", "kosher", "shabbat", "rabbi", "menorah", "mitzvah", "hanukkah",],
    'buddhism': ["buddhist", "buddhism", "monastery", "tripitaka", "pagoda", "vihara", "vesak", "monk", "buddha", "Sangha", "mandala", "dharma", "stupa"],
    'hinduism': ["hinduism", "hindu", "mandir", "bhagavad gita", "varanasi", "diwali", "holi", "puja", "Yajna", "murti", "moksha", "brahma", "vedas",],
}


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def collect_activation_texts(base_folder):
    """
    Traverse the base folder and extract activation tokens for religion-specific terms.

    Parameters
    ----------
    base_folder : str
        Root directory containing per-model outputs (default: "json5/").
    """

    # Loop over all model subfolders
    for model_folder in os.listdir(base_folder):
        model_folder_path = os.path.join(base_folder, model_folder)
        if os.path.isdir(model_folder_path):

            # Loop over all source subfolders (e.g., res-16k, att-16k)
            for source_folder in os.listdir(model_folder_path):
                source_folder_path = os.path.join(model_folder_path, source_folder)
                if os.path.isdir(source_folder_path):

                    # For each religion group (Christianity, Islam, etc.)
                    for query_set_name, query_terms in query_terms_sets.items():
                        # Prepare CSV output file path
                        csv_file_path = os.path.join(
                            source_folder_path, f'activation_analysis_{query_set_name}.csv'
                        )

                        # Open CSV for writing activations
                        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow(csv_columns)

                            # Iterate over all query folders (e.g., "This is a church")
                            for query_name in os.listdir(source_folder_path):
                                current_query_terms = query_name.split(' ')

                                # Check if any token in query matches the religion-specific terms
                                for current_query_term in current_query_terms:
                                    if current_query_term in query_terms:
                                        subfolder_path = os.path.join(source_folder_path, query_name)

                                        if os.path.isdir(subfolder_path):
                                            # Loop through all JSON files in the query subfolder
                                            for json_filename in os.listdir(subfolder_path):
                                                if json_filename.endswith('.json'):
                                                    json_filepath = os.path.join(subfolder_path, json_filename)

                                                    # Latent feature ID extracted from filename
                                                    latent_feature_number = json_filename.split('_')[-1].split('.')[0]

                                                    # Load JSON file
                                                    with open(json_filepath, 'r', encoding='utf-8') as json_file:
                                                        data = json.load(json_file)

                                                    # Case 1: JSON is a list of items
                                                    if isinstance(data, list):
                                                        for item in data:
                                                            activations = item.get('activations', [])
                                                            for activation in activations:
                                                                tokens = activation.get('tokens', [])
                                                                writer.writerow(
                                                                    [current_query_term, latent_feature_number, ' '.join(tokens)]
                                                                )
                                                    else:
                                                        # Case 2: JSON is a single object
                                                        activations = data.get('activations', [])
                                                        for activation in activations:
                                                            tokens = activation.get('tokens', [])
                                                            writer.writerow(
                                                                [current_query_term, latent_feature_number, ' '.join(tokens)]
                                                            )


if __name__ == "__main__":
    collect_activation_texts(base_folder)
