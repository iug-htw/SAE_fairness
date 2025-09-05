"""
step8a_count_overlapping_features_intragroup.py

This script implements Step 8 of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Count the number of **latent features shared across multiple queries** within a 
query group (e.g., religion-specific prompts).

For example: if the same latent feature activates for  
*"This is a Bible"*, *"This is a priest"*, and *"This is Christianity"*,  
it is counted as an overlapping feature.

This script supports the **intra-group overlap analysis (RQ1)**.

Workflow
--------
1. Traverse the directory structure (`base_folder/model/source/query/`).  
2. For each query in the group:
   - Collect the set of feature IDs from the corresponding JSON files.  
3. Count how many features appear in ≥ 2 queries of the group.  
4. Record results per model in `latent_feature_activation_counts.csv`.

Inputs
------
- model_sources : list of str  
    Models to include (e.g., "gemma-2-2b", "gpt2-small").  
- group_name : str  
    Label for the query group (e.g., "Christianity", "Islam").  
- query_groups : list of str  
    Queries to include in the group (e.g., "This is a bible", "This is a priest").  
- base_folder : str, default="json"  
    Root directory containing model/source/query JSON outputs.

Outputs
-------
- `latent_feature_activation_counts.csv`  
    A CSV file with rows = groups and columns = models.  
    Each cell contains the number of overlapping features for that model/group.

Notes
-----
- Overlaps are defined as **feature IDs that appear in two or more queries**.  
- Results are appended to the CSV, so multiple groups can be added sequentially.
"""

import os
import csv
import re


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def count_overlapping_features(model_sources, group_name, query_groups, base_folder='json'):
    """
    Count overlapping features across queries within a group.

    Parameters
    ----------
    model_sources : list of str
        Models to analyze.
    group_name : str
        Group label (e.g., "Christianity").
    query_groups : list of str
        List of query prompts for the group.
    base_folder : str, default="json"
        Root directory containing model/source/query outputs.

    Process
    -------
    - For each model:
        * Collect feature IDs for each query in the group.
        * Count features that appear in ≥ 2 queries.
    - Append results to `latent_feature_activation_counts.csv`.

    Output
    ------
    - Updates/creates CSV file with one row per group and one column per model.
    """

    output_file = os.path.join(base_folder, "latent_feature_activation_counts.csv")

    # Check if CSV already exists (to decide whether to write header)
    file_exists = os.path.isfile(output_file)

    # Store results per model
    results = {model: 0 for model in model_sources}

    # Loop through models
    for model in model_sources:
        model_path = os.path.join(base_folder, model)
        if not os.path.exists(model_path):
            continue

        # Loop through SAE source sets for this model
        for source in os.listdir(model_path):
            source_path = os.path.join(model_path, source)
            if not os.path.isdir(source_path):
                continue

            feature_sets = {}  # Map query → feature set

            # Collect features per query
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

            # Count how many queries each feature appears in
            feature_counts = {}
            for features in feature_sets.values():
                for feature in features:
                    feature_counts[feature] = feature_counts.get(feature, 0) + 1

            # Count features appearing in ≥ 2 queries
            overlapping_features = sum(1 for count in feature_counts.values() if count >= 2)
            results[model] += overlapping_features

    # Append results to CSV
    with open(output_file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Group Name"] + model_sources)  # Write header once
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

    count_overlapping_features(
        model_sources,
        group_name="Christianity",
        query_groups=[
            "This is a baptsim",  # typo preserved from input
            "This is a bible",
            "This is a christian",
            "This is a church",
            "This is a gospel",
            "This is a pope",
            "This is christianity",
            "This is jesus",
        ],
        base_folder="json5"
    )
