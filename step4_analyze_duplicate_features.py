import json
import csv
import os
from collections import defaultdict
# This script reads the output of the duplicate features detection script and analyzes the common features between terms.   
# uses duplicates_output.json file as input

def analyze_duplicates(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    term_features = defaultdict(set)
    
    for feature_id, paths in data['duplicates'].items():
        for path in paths:
            term = path.split('/')[-2]
            term_features[term].add(feature_id)
    
    common_features = defaultdict(int)
    common_features_three_terms = defaultdict(int)
    
    terms = list(term_features.keys())
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            for k in range(j + 1, len(terms)):
                common_count_three = len(term_features[terms[i]].intersection(term_features[terms[j]], term_features[terms[k]]))
                if common_count_three > 0:
                    common_features_three_terms[(terms[i], terms[j], terms[k])] = common_count_three
                    continue
            common_count = len(term_features[terms[i]].intersection(term_features[terms[j]]))
            if common_count > 0:
                common_features[(terms[i], terms[j])] = common_count
    
    return common_features, common_features_three_terms

def save_to_csv(common_features, common_features_three_terms, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Term1', 'Term2', 'Term3', 'CommonFeatures']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for terms, count in common_features.items():
            writer.writerow({'Term1': terms[0], 'Term2': terms[1], 'Term3': '', 'CommonFeatures': count})
        for terms, count in common_features_three_terms.items():
            writer.writerow({'Term1': terms[0], 'Term2': terms[1], 'Term3': terms[2], 'CommonFeatures': count})

def process_model_release(model_release):
    input_path = f'/workspaces/SAE_fairness/json/{model_release}/duplicates_output.json'
    output_path = f'/workspaces/SAE_fairness/json/{model_release}/common_features.csv'
    if os.path.exists(input_path):
        common_features, common_features_three_terms = analyze_duplicates(input_path)
        save_to_csv(common_features, common_features_three_terms, output_path)
        print(f"Common features for {model_release} saved to {output_path}")
    else:
        print(f"File {input_path} does not exist.")

if __name__ == "__main__":
    model_releases = ["llama3.1-8b-eleuther_gp", "llama-scope", "gemma-scope", "gpt2sm-apollojt", "gpt2sm-rfs-jb", "gpt2sm-kk", "llama3-8b-it-res-jh"]
    for model_release in model_releases:
        process_model_release(model_release)