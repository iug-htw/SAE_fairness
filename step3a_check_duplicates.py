import os
import re
import json
from collections import defaultdict

modelReleases = ["llama3.1-8b-eleuther_gp", "llama-scope","gemma-scope","gpt2sm-apollojt","gpt2sm-rfs-jb", "gpt2sm-kk", "llama3-8b-it-res-jh" ]

# this checks for duplicates in the feature numbers

def find_feature_numbers(directory):
    feature_pattern = re.compile(r'data_for_feature_(\d+)\.json')
    feature_files = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            match = feature_pattern.search(file)
            if match:
                feature_number = match.group(1)
                feature_files[feature_number].append(os.path.join(root, file))

    return feature_files

def check_for_duplicates(feature_files):
    duplicates = {k: v for k, v in feature_files.items() if len(v) > 1}
    return duplicates

def main():
    for modelRelease in modelReleases:
        directory = 'json/' + modelRelease
        feature_files = find_feature_numbers(directory)
        duplicates = check_for_duplicates(feature_files)
        output = {} # Output dictionary to write to JSON file

        if duplicates:
            output["message"] = "Duplicate feature numbers found:"
            output["duplicates"] = {}
            for feature_number, files in duplicates.items():
                output["duplicates"][feature_number] = files
                print(f"Feature number {feature_number} found in files:")
                for file in files:
                    print(f"  - {file}")
        else:
            print("No duplicate feature numbers found.")
        
        # Write output to a JSON file
        with open(directory+'/duplicates_output.json', 'w') as json_file:
            json.dump(output, json_file, indent=4)

if __name__ == "__main__":
    main()