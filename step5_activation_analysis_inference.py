# -*- coding: utf-8 -*-

import json
import csv
import os

# Step 5: Activation Analysis
# This script iterates through all subfolders in the "json4" folder, where each subfolder represents a model.
# For each model, it creates a CSV file named "activation_analysis.csv" in the respective model's folder.
# The script processes all JSON files in the subfolders of each model, extracting activation tokens and
# writing them to the CSV file along with the folder name, query term, and latent feature number.

# Define the base folder containing the model subfolders
base_folder = 'json5/'

# Define the CSV file columns
csv_columns = ['query_term', 'latent_feature_number', 'activation_tokens']

# Define the query terms to be used
query_terms_sets = {
    'christianity': ["baptism", "bible", "christian", "church", "gospel", "pope", "sacrament", "christianity", "jesus", "priest", "pastor", "crucifix", "communion",],
    'islam': ["burka", "hijab", "mosque", "muslim", "quran", "allah", "halal", "islam", "mecca", "imam", "ramadan", "eid", "hajj",],
    'judaism': ["jew", "kippah", "synagogue", "talmud", "torah", "judaism", "kosher", "shabbat", "rabbi", "menorah", "mitzvah", "hanukkah",],
    'buddhism': ["buddhist", "buddhism", "monastery", "tripitaka", "pagoda", "vihara", "vesak", "monk", "buddha", "Sangha", "mandala", "dharma", "stupa"],
    'hinduism': ["hinduism", "hindu", "mandir", "bhagavad gita", "varanasi", "diwali", "holi", "puja", "Yajna", "murti", "moksha", "brahma", "vedas",],
}


def activation_analysis_inference(base_folder):
    # Iterate through all model subfolders in the base folder
    for model_folder in os.listdir(base_folder):
        model_folder_path = os.path.join(base_folder, model_folder)
        if os.path.isdir(model_folder_path):
            # Iterate through all subfolders in the model folder
            for source_folder in os.listdir(model_folder_path):
                source_folder_path = os.path.join(model_folder_path, source_folder)
                if os.path.isdir(source_folder_path):
                    # Iterate through all sets of query terms
                    for query_set_name, query_terms in query_terms_sets.items():
                        # Define the CSV file path for the current model, source, and query set
                        csv_file_path = os.path.join(source_folder_path, f'activation_analysis_{query_set_name}.csv')
                        
                        # Write the data to the CSV file
                        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow(csv_columns)
                            
                            # Iterate through all subfolders in the source folder
                            for query_name in os.listdir(source_folder_path):
                                current_query_terms = query_name.split(' ')

                                for current_query_term in current_query_terms:
                                    if current_query_term in query_terms:
                                        subfolder_path = os.path.join(source_folder_path, query_name)
                                        
                                        if os.path.isdir(subfolder_path):
                                            # Iterate through all JSON files in the subfolder
                                            for json_filename in os.listdir(subfolder_path):
                                                if json_filename.endswith('.json'):
                                                    json_filepath = os.path.join(subfolder_path, json_filename)
                                                    
                                                    # Extract the latent feature number from the file name
                                                    latent_feature_number = json_filename.split('_')[-1].split('.')[0]
                                                    
                                                    # Load the JSON data
                                                    with open(json_filepath, 'r', encoding='utf-8') as json_file:
                                                        data = json.load(json_file)
                                                    
                                                    # Check if data is a list and iterate through it
                                                    if isinstance(data, list):
                                                        for item in data:
                                                            activations = item.get('activations', [])
                                                            for activation in activations:
                                                                tokens = activation.get('tokens', [])
                                                                writer.writerow([current_query_term, latent_feature_number, ' '.join(tokens)])
                                                    else:
                                                        # Extract the relevant information
                                                        activations = data.get('activations', [])
                                                        # Write the data to the CSV file
                                                        for activation in activations:
                                                            tokens = activation.get('tokens', [])
                                                            writer.writerow([current_query_term, latent_feature_number, ' '.join(tokens)])

if __name__ == "__main__":
    activation_analysis_inference(base_folder)