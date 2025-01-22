import json
import csv
import os
from collections import defaultdict

# This script reads the output of the duplicate features detection script and analyzes the common features between terms.
# uses duplicates_output4.json file as input

def analyze_duplicates(file_path):
    print(file_path)
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    term_features = defaultdict(set)
    
    for feature_id, paths in data.get('duplicates', {}).items():
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

def process_model_source_set(model, source):
    input_path = f'json4/{model}/{source}/duplicates_output4.json'
    output_path = f'json4/{model}/{source}/common_features.csv'
    if os.path.exists(input_path):
        common_features, common_features_three_terms = analyze_duplicates(input_path)
        if common_features or common_features_three_terms:
            save_to_csv(common_features, common_features_three_terms, output_path)
            print(f"Common features for {model}-{source} saved to {output_path}")
        else:
            print(f"No common features found for {model}-{source}.")
    else:
        print(f"File {input_path} does not exist.")

if __name__ == "__main__":
    model_source_sets = [
        ("gpt2-small", "res-jb"),#fertig
        ("gpt2-small", "att-kk"), #fertig
        #("gpt2-small", "att_32k-oai"), #bis programmer
        #("gpt2-small", "mlp_32k-oai"),bis programmer
        ("gemma-2-2b", "gemmascope-att-16k"),# fertig
        ("gemma-2-2b", "gemmascope-att-65k"),# fertig
        ("gemma-2-2b", "gemmascope-mlp-16k"),# fertig
        #("gemma-2-2b", "gemmascope-mlp-65k"), überspringen!
        #("gemma-2-2b", "gemmascope-res-16k"), überspringen!
        #("gemma-2-2b", "gemmascope-res-65k"), überspringen!
        #("gemma-2-9b", "gemmascope-res-16k"), überspringen!
        #("gemma-2-9b-it", "gemmascope-res-16k"), überspringen!
        ("gemma-2-9b-it", "gemmascope-res-131k"),  # fertig
        ("llama3.1-8b","llamascope-res-32k"),# fertig
    ]
    for model, source in model_source_sets:
        process_model_source_set(model, source)
