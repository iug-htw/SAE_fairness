"""
step3a_check_duplicates_inference.py

This script implements Step 3a of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Detect and aggregate **latent features that activate for multiple queries**.  

Workflow
--------
1. Traverse the directory structure created in previous steps.
2. Identify feature JSON files (`data_for_feature_<id>.json`) by their feature index.
3. For each feature:
   - Collect all queries where it appeared.
   - Detect cases where the same feature index was triggered by multiple queries.
4. Save results to a JSON file (`duplicates_output.json`) listing shared features and their query sets.

Notes
-----
- A "duplicate" here does not mean a data error.  
- Instead, it represents **conceptual overlap**: the same latent feature 
  firing for multiple queries (potentially across the same religion group).
- This script is part of the **Data Analysis phase** of the pipeline.
"""

import os
import re
import json
from collections import defaultdict


# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def find_feature_numbers(directory):
    """ Traverse a directory and collect all feature JSON files by feature index. """
    feature_pattern = re.compile(r'^data_for_feature_(\d+)\.json$')
    feature_files = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            match = feature_pattern.search(file)
            if match:
                feature_number = match.group(1)
                # Normalize path separators for consistency
                feature_files[feature_number].append(
                    os.path.join(root, file).replace('\\', '/')
                )

    return feature_files


def check_for_duplicates(feature_files):
    """ Identify features that appear in more than one file (shared across queries). """

    return {k: v for k, v in feature_files.items() if len(v) > 1}


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def check_duplicates_inference(modelReleases, main_dir='json'):
    """
    Run duplicate feature detection across all models and sources.

    Parameters
    ----------
    modelReleases : list of str
        Model names to process.
    main_dir : str
        Root directory containing JSON feature files (from Step 1/2).

    Process
    -------
    - For each model and residual source directory:
      * Find feature files.
      * Detect duplicates (features active for multiple queries).
      * Extract the query names where overlaps occurred.
      * Save results to `duplicates_output.json` in the same directory.

    Output Example
    --------------
    {
        "message": "Duplicate feature numbers found:",
        "duplicates": {
            "20701": ["This is a church", "This is a Bible"],
            "19432": ["This is Islam", "This is the Quran"]
        }
    }
    """
    for model in modelReleases:
        # Explore all source set directories for the model
        files = os.listdir(os.path.join(main_dir, model))

        for source in files:
            directory = f'{main_dir}/{model}/{source}'
            feature_files = find_feature_numbers(directory)
            duplicates = check_for_duplicates(feature_files)

            output = {}  # JSON output structure
            if duplicates:
                output["message"] = "Duplicate feature numbers found:"
                output["duplicates"] = {}

                for feature_number, duplicates_files in duplicates.items():
                    # Extract query names from paths (directory level)
                    query_paths = []
                    for file_path in duplicates_files:
                        parts = file_path.split('/')
                        if len(parts) >= 4:
                            query = parts[3]  # directory name = query string
                            query_paths.append(query)

                    output["duplicates"][feature_number] = query_paths

                print(f"✅ {len(duplicates.items())} duplicate feature numbers found. {model} => {source}")
            else:
                print(f"❗No duplicate feature numbers found. {model} => {source}")

            # Ensure directory exists before saving
            os.makedirs(directory, exist_ok=True)

            # Write results to file
            with open(os.path.join(directory, 'duplicates_output.json'), 'w') as json_file:
                json.dump(output, json_file, indent=4)


if __name__ == "__main__":
    model_sources = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]

    check_duplicates_inference(model_sources, main_dir="json6")
