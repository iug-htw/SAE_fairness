import os
import csv
import re

def count_intergroup_overlap(model_sources, group_name, group1_queries, group2_queries, base_folder='json'):
    output_file = os.path.join(base_folder, "latent_feature_activation_counts.csv")

    # Check if output file already exists
    file_exists = os.path.isfile(output_file)

    results = {model: 0 for model in model_sources}  # Store overlap counts per model

    for model in model_sources:
        model_path = os.path.join(base_folder, model)
        if not os.path.exists(model_path):
            continue

        group1_features = set()
        group2_features = set()

        for source in os.listdir(model_path):
            source_path = os.path.join(model_path, source)
            if not os.path.isdir(source_path):
                continue

            for query in os.listdir(source_path):
                query_path = os.path.join(source_path, query)
                if not os.path.isdir(query_path):
                    continue

                feature_numbers = set()
                for file in os.listdir(query_path):
                    match = re.match(r"data_for_feature_(\d+)\.json", file)
                    if match:
                        feature_numbers.add(int(match.group(1)))

                if query in group1_queries:
                    group1_features.update(feature_numbers)
                elif query in group2_queries:
                    group2_features.update(feature_numbers)

        # Count overlapping features
        overlapping_features = len(group1_features.intersection(group2_features))
        results[model] = overlapping_features

    # Write results to CSV
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

    group1 = [
        "This is a baptism",
        "This is a bible",
        "This is a christian",
        "This is a church",
        "This is a gospel",
        "This is a pope",
        "This is christianity",
        "This is jesus",
    ]

    group2 = [
        "This is a mosque",
        "This is the quran",
        "This is a muslim",
        "This is an imam",
        "This is islam",
        "This is ramadan",
        "This is allah",
        "This is muhammad",
    ]

    count_intergroup_overlap(model_sources, group_name="Christianity_vs_Islam", group1_queries=group1, group2_queries=group2, base_folder="json5")
