"""
step4b_combine_csv_inference.py

This script implements Step 4b of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Aggregate per-model `common_features.csv` outputs into a single comparative CSV.  
Each input file contains counts of **latent features shared across a set of three queries**.  
By combining them, we can directly compare overlap patterns across all models and SAE sources.

Workflow
--------
1. For each (model, source) pair:
   - Locate the file `<main_dir>/<model>/<source>/common_features.csv`.
   - Read all rows, each representing a query triplet (`Term1`, `Term2`, `Term3`) and the number of common features.
   - Store counts keyed by the triplet.

2. Merge results from all models:
   - Each row in the final CSV corresponds to a unique (`Term1`, `Term2`, `Term3`) combination.
   - Columns show feature counts for each model-source pair.

3. Save merged results to:
   - `<main_dir>/combined_common_features.csv`
"""

import os
import csv


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def combine_csv_files(model_sources, main_dir="json"):
    """
    Combine per-model `common_features.csv` files into one unified CSV.

    Parameters
    ----------
    model_sources : list of str
        Model names to process (each must have one or more source subdirectories).
    main_dir : str, default="json"
        Root directory containing per-model source folders with `common_features.csv`.

    Workflow
    --------
    - Iterate through `<main_dir>/<model>/<source>/common_features.csv`
    - Collect feature counts for each (`Term1`, `Term2`, `Term3`) triplet.
    - Merge results across models, aligning rows by triplet.

    Output
    ------
    A CSV file saved at `<main_dir>/combined_common_features.csv` with:

    - Columns: `Term1`, `Term2`, `Term3` + one column per model-source pair
    - Rows: each unique query triplet across all models
    - Values: counts of shared latent features (default 0 if not found)

    Example row
    -----------
    Term1 = "This is Quran", Term2 = "This is Islam", Term3 = "This is a terrorist"

    gemma-2-2b-res-16k | gemma-2-9b-res-16k | gpt2-small-res-jb | ...
    12                 |  8                 |  14               | ...
    """

    model_sources_sets = []
    for model in model_sources:
        files = os.listdir(os.path.join(main_dir, model))
        for source in files:
            model_sources_sets.append((model, source))

    combined_data = {}
    
    for model, source in model_sources_sets:
        input_path = f'{main_dir}/{model}/{source}/common_features.csv'
        if os.path.exists(input_path):
            with open(input_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    term_pair = (row['Term1'], row['Term2'], row['Term3'])
                    if term_pair not in combined_data:
                        combined_data[term_pair] = {}
                    combined_data[term_pair][f'{model}-{source}'] = row['CommonFeatures']
        else:
            print(f"File {input_path} does not exist.")
    
    output_path = f'{main_dir}/combined_common_features.csv'
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Term1', 'Term2', 'Term3'] + [f'{model}-{source}' for model, source in model_sources_sets]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for term_pair, features in combined_data.items():
            row = {'Term1': term_pair[0], 'Term2': term_pair[1], 'Term3': term_pair[2]}
            for model, source in model_sources_sets:
                row[f'{model}-{source}'] = features.get(f'{model}-{source}', 0)
            writer.writerow(row)

    print(f"✅ Combined CSV saved to {output_path}")

if __name__ == "__main__":
    model_sources = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]

    output_path = 'json4/combined_common_features.csv'
    combine_csv_files(model_sources, main_dir="json4")
    print(f"Combined CSV saved to {output_path}")
