"""
step8c_count_cosine_sim_intergroup.py

This script implements Step 8c of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Compute **cosine similarity** between two groups of queries (e.g., Islam vs. Terrorism) 
based on their latent feature activations across different SAEs.

While Step 8a/8b counted overlapping features directly, this step provides a 
vector-based similarity measure that accounts for the entire feature space.

The results from this step were not included in the final paper
as the results were too noisy due to extreme sparsity.

Workflow
--------
1. Traverse `base_folder/model/source/query/`.  
2. For each SAE source set:
   - Create a binary vector (length = SAE size) for group1 and group2.  
   - Each index is set to 1 if the corresponding feature is activated by at least one query.  
3. Compute cosine similarity between group1 and group2 vectors.  
4. Record similarity scores for each (model, source).  

Inputs
------
- model_sources : list of str  
    Models to analyze (e.g., "gemma-2-2b").  
- sae_source_sizes : list of tuples  
    Each tuple defines (source_folder_name, feature_space_size).  
- group_name : str  
    Label for the comparison (e.g., "Islam_vs_Terrorism").  
- group1_queries : list of str  
    Queries belonging to group1.  
- group2_queries : list of str  
    Queries belonging to group2.  
- base_folder : str, default="json"  
    Root directory containing model/source/query JSON outputs.  

Outputs
-------
- `latent_feature_cosine_similarities.csv`  
    A CSV file with rows = group comparisons and columns = (model:source).  
    Each cell contains the cosine similarity score between two query groups.

Notes
-----
- Cosine similarity ∈ [0,1]:
  * 0 = no overlap in feature space  
  * 1 = perfect alignment (identical features)  
- Provides a more nuanced measure of similarity than simple overlap counts (Steps 8a/8b).
"""

import os
import csv
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def compute_cosine_intergroup_similarity(model_sources, sae_source_sizes, group_name, group1_queries, group2_queries, base_folder='json'):
    """
    Compute cosine similarity between two groups of queries.

    Parameters
    ----------
    model_sources : list of str
        Models to analyze.
    sae_source_sizes : list of tuples
        Each tuple is (source_name, SAE size).
    group_name : str
        Label for the group comparison.
    group1_queries : list of str
        Queries for group1.
    group2_queries : list of str
        Queries for group2.
    base_folder : str, default="json"
        Root directory containing model/source/query outputs.

    Process
    -------
    - For each (model, SAE):
        * Collect feature IDs for group1 and group2.
        * Build binary activation vectors of length = SAE size.
        * Compute cosine similarity between the vectors.
    - Append results to `latent_feature_cosine_similarities.csv`.

    Output
    ------
    - CSV file with similarity scores for each (model:SAE) pair.
    """
    
    output_file = os.path.join(base_folder, "latent_feature_cosine_similarities.csv")
    file_exists = os.path.isfile(output_file)
    results = {model: {} for model in model_sources}

    # Map source name -> SAE size
    sae_size_dict = dict(sae_source_sizes)

    for model in model_sources:
        model_path = os.path.join(base_folder, model)
        if not os.path.exists(model_path):
            continue

        for source in os.listdir(model_path):
            source_path = os.path.join(model_path, source)
            if not os.path.isdir(source_path):
                continue

            if source not in sae_size_dict:
                print(f"Skipping unknown SAE source: {source}")
                continue

            sae_size = sae_size_dict[source]
            group1_vector = np.zeros(sae_size)
            group2_vector = np.zeros(sae_size)
            group1_features = set()
            group2_features = set()

            # Collect feature IDs for each query
            for query in os.listdir(source_path):
                query_path = os.path.join(source_path, query)
                if not os.path.isdir(query_path):
                    continue

                feature_ids = set()
                for file in os.listdir(query_path):
                    match = re.match(r"data_for_feature_(\d+)\.json", file)
                    if match:
                        feature_ids.add(int(match.group(1)))

                if query in group1_queries:
                    group1_features.update(feature_ids)
                elif query in group2_queries:
                    group2_features.update(feature_ids)

            # Encode feature sets into binary vectors
            for idx in group1_features:
                if idx < sae_size:
                    group1_vector[idx] = 1
            for idx in group2_features:
                if idx < sae_size:
                    group2_vector[idx] = 1

            # Compute cosine similarity
            sim = cosine_similarity([group1_vector], [group2_vector])[0][0]
            results[model][source] = round(sim, 4)

    # Append results to CSV
    with open(output_file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            header = ["Group Name"]
            for model in model_sources:
                header += [f"{model}:{source}" for source in results[model].keys()]
            writer.writerow(header)

        row = [group_name]
        for model in model_sources:
            row += [results[model].get(source, "NA") for source in results[model]]
        writer.writerow(row)

    print("Cosine similarity results appended to", output_file)


if __name__ == "__main__":
    model_sources = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]

    # Each tuple: (SAE source folder, latent dimension size)
    sae_source_sizes = [
        ("gemmascope-res-16k", 16384),
        ("gemmascope-att-16k", 16384),
        ("gemmascope-res-65k", 65536),
        ("gemmascope-res-131k", 131072),
        ("llamascope-res-32k", 32768),
        ("res-jb", 24576),
        ("att-kk", 24576),
    ]

    # Example groups: Islam vs Terrorism
    group1 = [
        "This is a mosque", "This is the quran", "This is a muslim",
        "This is an imam", "This is islam", "This is ramadan",
        "This is allah", "This is muhammad"
    ]

    group2 = [
        "This is a terrorist", "This is extremism", "This is a crime",
        "This is a bombing", "This is an attack", "This is violence"
    ]

    compute_cosine_intergroup_similarity(
        model_sources,
        sae_source_sizes,
        group_name="Islam_vs_Terrorism",
        group1_queries=group1,
        group2_queries=group2,
        base_folder="json5"
    )
