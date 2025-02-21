import os
import re
import json
from collections import defaultdict

# this checks for duplicates in the feature numbers

def find_feature_numbers(directory):
    feature_pattern = re.compile(r'^data_for_feature_(\d+)\.json$')
    feature_files = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            match = feature_pattern.search(file)
            if match:
                feature_number = match.group(1)
                # Use forward slashes for the JSON paths
                feature_files[feature_number].append(os.path.join(root, file).replace('\\', '/'))

    return feature_files

def check_for_duplicates(feature_files):
    duplicates = {k: v for k, v in feature_files.items() if len(v) > 1}
    return duplicates

def check_duplicates_inference(modelReleases, main_dir='json'):
    for model in modelReleases:
        # list out all files in the main_dir/{modelRelease}/{query}/
        files = os.listdir(os.path.join(main_dir, model))

        for source in files:
            directory = f'{main_dir}/{model}/{source}'
            feature_files = find_feature_numbers(directory)
            duplicates = check_for_duplicates(feature_files)
            output = {} # Output dictionary to write to JSON file

            if duplicates:
                output["message"] = "Duplicate feature numbers found:"
                output["duplicates"] = {}
                for feature_number, duplicates_files in duplicates.items():
                    # Extract query names from paths
                    query_paths = []
                    for file_path in duplicates_files:
                        # Split path and get the query part (4th element when splitting by '/')
                        parts = file_path.split('/')
                        if len(parts) >= 4:
                            query = parts[3]  # This will get "I learn programming" from the path
                            query_paths.append(query)
                    output["duplicates"][feature_number] = query_paths
                print(f"✅ {len(duplicates.items())} duplicate feature numbers found. {model} => {source}")
                
            else:
                print("❗No duplicate feature numbers found. {model} => {source}")
            
            # Ensure the directory exists before writing the JSON file
            os.makedirs(directory, exist_ok=True)
            
            # Write output to a JSON file
            with open(directory+'/duplicates_output5.json', 'w') as json_file:
                json.dump(output, json_file, indent=4)

if __name__ == "__main__":
    check_duplicates_inference()