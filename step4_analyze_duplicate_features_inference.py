import json
import csv
import os
from collections import defaultdict

# This script reads the output of the duplicate features detection script and analyzes the common features between terms.
# uses duplicates_output4.json file as input

def analyze_duplicates(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    term_features = defaultdict(set)
    
    for feature_id, terms in data.get('duplicates', {}).items():
        for term in terms:
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

def analyze_duplicate_features(modelReleases, main_dir="json"):
    for model in modelReleases:
        files = os.listdir(os.path.join(main_dir, model))

        for source in files:
            input_path = f'{main_dir}/{model}/{source}/duplicates_output5.json'
            output_path = f'{main_dir}/{model}/{source}/common_features.csv'
            if os.path.exists(input_path):
                common_features, common_features_three_terms = analyze_duplicates(input_path)
                if common_features or common_features_three_terms:
                    save_to_csv(common_features, common_features_three_terms, output_path)
                    print(f"✅ Common features for {model}-{source} saved.")
                else:
                    print(f"❗ No common features found for {model}-{source}.")
            else:
                print(f"❗ File {input_path} does not exist.")

if __name__ == "__main__":
    model_sources = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]
    
    analyze_duplicate_features(model_sources, main_dir="json6")
