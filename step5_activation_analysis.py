import json
import csv
import os

# Step 5: Activation Analysis
# This script iterates through all subfolders in the "json" folder, where each subfolder represents a model.
# For each model, it creates a CSV file named "activation_analysis.csv" in the respective model's folder.
# The script processes all JSON files in the subfolders of each model, extracting activation tokens and
# writing them to the CSV file along with the folder name, query term, and latent feature number.

# Define the base folder containing the model subfolders
base_folder = 'json/'

# Define the CSV file columns
csv_columns = ['query_term', 'latent_feature_number', 'activation_tokens']

# Define the query terms to be used
#query_terms = ['muslim', 'islam', 'mosque', 'allah', 'quran', 'mekka', 'hijab', 'burka', 'halal']
#query_terms = ['christian', 'christianity', 'church', 'pope', 'bible', 'jesus', 'gospel', 'baptism', 'sacrament']
query_terms = ['jew', 'judaism', 'synagogue', 'temple', 'torah', 'shabbat', 'kippah', 'kosher', 'talmud']
#query_terms = ['Mädchen', 'Junge', 'Mann', 'Frau', 'Oma', 'Opa']
#query_terms = ['male', 'boy', 'grandpa', 'man', 'king', 'gentleman', 'he', 'husband', 'son']
#query_terms = ['female', 'girl', 'grandma', 'woman', 'queen', 'lady', 'she', 'wife', 'daughter']
#query_terms = ['teacher', 'nurse', 'assistant', 'receptionist', 'midwife', 'homemaker']
#query_terms = ['professor', 'doctor', 'boss', 'engineer', 'firefighter', 'programmer']


# Iterate through all model subfolders in the base folder
for model_folder in os.listdir(base_folder):
    model_folder_path = os.path.join(base_folder, model_folder)
    if os.path.isdir(model_folder_path):
        # Define the CSV file path for the current model
        csv_file_path = os.path.join(model_folder_path, 'activation_analysis_judaism.csv')
        
        # Write the data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_columns)
            
            # Iterate through all subfolders in the model folder
            for subfolder in os.listdir(model_folder_path):
                if subfolder in query_terms:
                    subfolder_path = os.path.join(model_folder_path, subfolder)
                    if os.path.isdir(subfolder_path):
                        # Iterate through all JSON files in the subfolder
                        for json_filename in os.listdir(subfolder_path):
                            if json_filename.endswith('.json'):
                                json_filepath = os.path.join(subfolder_path, json_filename)
                                
                                # Extract the latent feature number from the file name
                                latent_feature_number = json_filename.split('_')[-1].split('.')[0]
                                
                                # Load the JSON data
                                with open(json_filepath, 'r') as json_file:
                                    data = json.load(json_file)
                                
                                # Check if data is a list and iterate through it
                                if isinstance(data, list):
                                    for item in data:
                                        activations = item.get('activations', [])
                                        for activation in activations:
                                            tokens = activation.get('tokens', [])
                                            writer.writerow([subfolder, latent_feature_number, ' '.join(tokens)])
                                else:
                                    # Extract the relevant information
                                    activations = data.get('activations', [])
                                    # Write the data to the CSV file
                                    for activation in activations:
                                        tokens = activation.get('tokens', [])
                                        writer.writerow([subfolder, latent_feature_number, ' '.join(tokens)])
