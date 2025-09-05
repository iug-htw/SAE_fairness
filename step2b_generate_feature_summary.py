"""
step2b_generate_feature_summary.py

This script implements a utility step of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Traverse the per-model/SAE/query directory structure and generate a **summary CSV** 
that indexes all latent feature JSON files collected in earlier steps.

The summary provides a compact reference mapping:
- Model name
- SAE source set
- Query string
- Latent feature number

Workflow
--------
1. Traverse `base_folder/` (default: json5), which contains model subfolders.
2. For each model → SAE → query → JSON file:
   - Extract latent feature number from the filename.
   - Record (model, SAE, query, feature number).
3. Save all results to `feature_summary.csv`.

Notes
-----
- This script does not perform analysis itself but creates an **index table** 
  that can be used to quickly query which features were collected where.
- Useful for sanity checks, dataset statistics, or debugging feature coverage.
"""

import os
import csv

# Define the CSV file columns
csv_columns = ['model', 'SAE', 'query', 'featurenumber']


def generate_feature_summary(base_folder="json"):
    """
    Generate a summary CSV indexing all feature JSONs.

    Parameters
    ----------
    base_folder : str
        Root directory containing model → SAE → query subfolders.

    Process
    -------
    - Walk through the directory structure:
        base_folder / model / SAE / query / data_for_feature_<id>.json
    - Extract the latent feature number from each filename.
    - Append metadata (model, SAE, query, feature number) to the summary list.
    - Save results as `feature_summary.csv`.

    Output
    ------
    - CSV with columns: model, SAE, query, featurenumber
    """
    output_csv_path = f'{base_folder}/feature_summary.csv'
    summary_data = []

    # Traverse model subfolders
    for model_folder in os.listdir(base_folder):
        model_folder_path = os.path.join(base_folder, model_folder)
        if os.path.isdir(model_folder_path):

            # Traverse SAE subfolders
            for sae_folder in os.listdir(model_folder_path):
                sae_folder_path = os.path.join(model_folder_path, sae_folder)
                if os.path.isdir(sae_folder_path):

                    # Traverse query subfolders
                    for query_folder in os.listdir(sae_folder_path):
                        query_folder_path = os.path.join(sae_folder_path, query_folder)
                        if os.path.isdir(query_folder_path):

                            # Traverse JSON feature files
                            for json_filename in os.listdir(query_folder_path):
                                if json_filename.endswith('.json'):
                                    # Extract feature number from filename
                                    featurenumber = json_filename.split('_')[-1].split('.')[0]

                                    # Collect metadata
                                    summary_data.append({
                                        'model': model_folder,
                                        'SAE': sae_folder,
                                        'query': query_folder,
                                        'featurenumber': featurenumber
                                    })

    # Write summary CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for row in summary_data:
            writer.writerow(row)

    print(f"Feature summary CSV saved to {output_csv_path}")


if __name__ == "__main__":
    base_folder = 'json5'
    generate_feature_summary(base_folder)
