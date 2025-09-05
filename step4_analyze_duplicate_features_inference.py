"""
step4a_analyze_duplicates.py

This script implements Step 4a of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Process the outputs of Step 3a (`duplicates_output.json`) to identify **common latent features** 
shared across pairs or triplets of queries.  
This allows us to quantify overlap between queries and prepare results for aggregation in Step 4b.

Workflow
--------
1. Load `duplicates_output.json` (produced by Step 3a) for each model/source.
   - Each entry contains a feature ID and the list of queries where that feature was active.

2. Build a mapping from query → set of activated features.

3. Compute overlaps:
   - **Pairs of queries**: number of features shared between two queries.
   - **Triplets of queries**: number of features shared across three queries.

4. Save results to `common_features.csv` for each model/source.

"""

import json
import csv
import os
from collections import defaultdict


def analyze_duplicates(file_path):
    """
    Analyze duplicate features for a given model/source.

    Parameters
    ----------
    file_path : str
        Path to `duplicates_output.json` containing feature-to-query mappings.

    Returns
    -------
    common_features : dict
        Mapping (term1, term2) → number of shared features.
    common_features_three_terms : dict
        Mapping (term1, term2, term3) → number of shared features.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Build query → set of features mapping
    term_features = defaultdict(set)
    for feature_id, terms in data.get('duplicates', {}).items():
        for term in terms:
            term_features[term].add(feature_id)

    common_features = defaultdict(int)
    common_features_three_terms = defaultdict(int)

    terms = list(term_features.keys())
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            # Check triplets
            for k in range(j + 1, len(terms)):
                common_count_three = len(
                    term_features[terms[i]].intersection(
                        term_features[terms[j]], term_features[terms[k]]
                    )
                )
                if common_count_three > 0:
                    common_features_three_terms[(terms[i], terms[j], terms[k])] = common_count_three
                    continue

            # Check pairs
            common_count = len(term_features[terms[i]].intersection(term_features[terms[j]]))
            if common_count > 0:
                common_features[(terms[i], terms[j])] = common_count

    return common_features, common_features_three_terms


def save_to_csv(common_features, common_features_three_terms, output_path):
    """
    Save common feature results to a CSV file.

    Parameters
    ----------
    common_features : dict
        Pairwise overlaps { (term1, term2): count }
    common_features_three_terms : dict
        Triple overlaps { (term1, term2, term3): count }
    output_path : str
        Output CSV path.

    Output Format
    -------------
    Term1 | Term2 | Term3 | CommonFeatures
    """
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Term1', 'Term2', 'Term3', 'CommonFeatures']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for terms, count in common_features.items():
            writer.writerow({
                'Term1': terms[0],
                'Term2': terms[1],
                'Term3': '',
                'CommonFeatures': count
            })
        for terms, count in common_features_three_terms.items():
            writer.writerow({
                'Term1': terms[0],
                'Term2': terms[1],
                'Term3': terms[2],
                'CommonFeatures': count
            })

# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def analyze_duplicate_features(modelReleases, main_dir="json"):
    """
    Main function: analyze duplicates for all models/sources.

    Parameters
    ----------
    modelReleases : list of str
        Models to process.
    main_dir : str
        Root directory containing model/source outputs.

    Process
    -------
    - For each model and source:
      * Load `duplicates_output.json`
      * Compute pairwise and triplet overlaps
      * Save results as `common_features.csv`
    """
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
