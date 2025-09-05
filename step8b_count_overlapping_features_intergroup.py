"""
step8b_count_overlapping_features_intergroup.py

This script implements Step 8b of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Measure the number of **latent features shared between two distinct query groups**.  
For example, the overlap between queries about *Christianity* and queries about *Islam*, 
or between *religion-related queries* and *violence-related queries*.

This analysis supports the **inter-group overlap analysis (RQ2)** by quantifying 
to what extent concepts from one group share internal representations with another.

Workflow
--------
1. Traverse the directory structure (`base_folder/model/source/query/`).  
2. For each query in group1 and group2:
   - Collect the set of feature IDs from the corresponding JSON files.  
3. Count the number of features that appear in **both groups**.  
4. Record overlap counts per model in `latent_feature_activation_counts.csv`.

Inputs
------
- model_sources : list of str  
    Models to include (e.g., "gemma-2-2b", "gpt2-small").  
- group_name : str  
    Label for the comparison (e.g., "Christianity_vs_Islam").  
- group1_queries : list of str  
    Queries defining the first group (e.g., Christianity-related).  
- group2_queries : list of str  
    Queries defining the second group (e.g., Islam-related).  
- base_folder : str, default="json"  
    Root directory containing model/source/query JSON outputs.

Outputs
-------
- `latent_feature_activation_counts.csv`  
    A CSV file with rows = group comparisons and columns = models.  
    Each cell contains the number of overlapping features for that comparison.  

Notes
-----
- Overlaps are defined as **feature IDs appearing in at least one query from each group**.  
- Results are appended to the same CSV as the intra-group analysis (Step 8), 
  ensuring both can be compared directly.
"""

import os
import csv
import re


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def count_intergroup_overlap(model_sources, group_name, group1_queries, group2_queries, base_folder='json'):
    """
    Count overlapping features between two groups of queries.

    Parameters
    ----------
    model_sources : list of str
        Models to analyze.
    group_name : str
        Label for the comparison (e.g., "Christianity_vs_Islam").
    group1_queries : list of str
        Queries belonging to the first group.
    group2_queries : list of str
        Queries belonging to the second group.
    base_folder : str, default="json"
        Root directory containing model/source/query outputs.

    Process
    -------
    - For each model:
        * Collect all feature IDs for queries in group1.
        * Collect all feature IDs for queries in group2.
        * Compute intersection of the two sets.
    - Append overlap counts to `latent_feature_activation_counts.csv`.

    Output
    ------
    - Updates/creates CSV file with one row per group comparison and one column per model.
    """
    output_file = os.path.join(base_folder, "latent_feature_activation_counts.csv")

    # Check if CSV already exists
    file_exists = os.path.isfile(output_file)

    # Store results per model
    results = {model: 0 for model in model_sources}

    # Loop through models
    for model in model_sources:
        model_path = os.path.join(base_folder, model)
        if not os.path.exists(model_path):
            continue

        group1_features = set()
        group2_features = set()

        # Loop through SAE source sets for this model
        for source in os.listdir(model_path):
            source_path = os.path.join(model_path, source)
            if not os.path.isdir(source_path):
                continue

            # Loop through queries
            for query in os.listdir(source_path):
                query_path = os.path.join(source_path, query)
                if not os.path.isdir(query_path):
                    continue

                feature_numbers = set()
                for file in os.listdir(query_path):
                    match = re.match(r"data_for_feature_(\d+)\.json", file)
                    if match:
                        feature_numbers.add(int(match.group(1)))

                # Assign features to group1 or group2
                if query in group1_queries:
                    group1_features.update(feature_numbers)
                elif query in group2_queries:
                    group2_features.update(feature_numbers)

        # Count overlaps between groups
        overlapping_features = len(group1_features.intersection(group2_features))
        results[model] = overlapping_features

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

    # Example: Christianity vs Islam
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

    count_intergroup_overlap(
        model_sources,
        group_name="Christianity_vs_Islam",
        group1_queries=group1,
        group2_queries=group2,
        base_folder="json5"
    )
