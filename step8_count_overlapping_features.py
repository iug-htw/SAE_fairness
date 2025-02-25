import os
import csv
import re

def count_overlapping_features(model_sources, group_name, query_groups, base_folder='json'):
    output_file = os.path.join(base_folder, "latent_feature_activation_counts.csv")
    
    # Read existing data to avoid duplicating headers
    file_exists = os.path.isfile(output_file)
    
    results = {model: 0 for model in model_sources}  # Store counts per model
    
    for model in model_sources:
        model_path = os.path.join(base_folder, model)
        if not os.path.exists(model_path):
            continue
        
        for source in os.listdir(model_path):
            source_path = os.path.join(model_path, source)
            if not os.path.isdir(source_path):
                continue
            
            feature_sets = {}  # Store feature numbers per query
            
            for query in os.listdir(source_path):
                if query not in query_groups:
                    continue
                
                query_path = os.path.join(source_path, query)
                if not os.path.isdir(query_path):
                    continue
                
                feature_numbers = set()
                for file in os.listdir(query_path):
                    match = re.match(r"data_for_feature_(\d+)\.json", file)
                    if match:
                        feature_numbers.add(int(match.group(1)))
                
                feature_sets[query] = feature_numbers
            
            # Count overlapping features
            all_features = [features for features in feature_sets.values()]
            feature_counts = {}
            for features in all_features:
                for feature in features:
                    feature_counts[feature] = feature_counts.get(feature, 0) + 1
            
            # Count features appearing in 2 or more queries
            overlapping_features = sum(1 for count in feature_counts.values() if count >= 2)
            results[model] += overlapping_features
    
    # Append results to CSV
    with open(output_file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Group Name"] + model_sources)  # Header row
        writer.writerow([group_name] + [results[model] for model in model_sources])
    
    print("Results appended to", output_file)

if __name__ == "__main__":
    model_sources = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]

    count_overlapping_features(model_sources, group_name="Christianity", query_groups=[
    "This is a baptsim",
    "This is a bible",
    "This is a christian",
    "This is a church",
    "This is a gospel",
    "This is a pope",
    "This is christianity",
    "This is jesus",], base_folder="json5")
