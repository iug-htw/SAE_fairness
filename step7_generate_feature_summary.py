import os
import csv

# Define the base folder containing the model subfolders
base_folder = 'json6/'

# Define the CSV file columns
csv_columns = ['model', 'SAE', 'query', 'featurenumber']

# Define the output CSV file path
output_csv_path = 'json6/feature_summary.csv'

# Initialize a list to store the summary data
summary_data = []

# Iterate through all model subfolders in the base folder
for model_folder in os.listdir(base_folder):
    model_folder_path = os.path.join(base_folder, model_folder)
    if os.path.isdir(model_folder_path):
        # Iterate through all SAE subfolders in the model folder
        for sae_folder in os.listdir(model_folder_path):
            sae_folder_path = os.path.join(model_folder_path, sae_folder)
            if os.path.isdir(sae_folder_path):
                # Iterate through all query subfolders in the SAE folder
                for query_folder in os.listdir(sae_folder_path):
                    query_folder_path = os.path.join(sae_folder_path, query_folder)
                    if os.path.isdir(query_folder_path):
                        # Iterate through all JSON files in the query folder
                        for json_filename in os.listdir(query_folder_path):
                            if json_filename.endswith('.json'):
                                json_filepath = os.path.join(query_folder_path, json_filename)
                                
                                # Extract the latent feature number from the file name
                                featurenumber = json_filename.split('_')[-1].split('.')[0]
                                
                                # Append the data to the summary list
                                summary_data.append({
                                    'model': model_folder,
                                    'SAE': sae_folder,
                                    'query': query_folder,
                                    'featurenumber': featurenumber
                                })

# Write the summary data to a CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for row in summary_data:
        writer.writerow(row)

print(f"Feature summary CSV saved to {output_csv_path}")
