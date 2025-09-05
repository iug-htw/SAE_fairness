"""
step3b_analyze_positive_logits.py

This script implements an exploratory analysis step for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Analyze **positive activation strings** (returned by SAEs) across all queries and detect duplicates.
If the same positive string appears for multiple queries, this may suggest recurring semantic patterns.

Workflow
--------
1. Traverse structured feature outputs (`logits_and_description_<query>.json` from Step 2).
2. Collect all positive strings with metadata (query, feature index, description).
3. Count how many times each string occurs across queries.
4. Save:
   - `duplicates_pos_count.json`: counts of repeated positive strings
   - `duplicates_pos_info.json`: detailed mapping of repeated strings to queries and feature indices

Note: This step was exploratory and not included in the final paper, 
as the results were not sufficiently descriptive. 
It is preserved here for completeness and potential future work.
"""

import json
import os
from collections import Counter


# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------


def load_json_file(filename):
    """Load a JSON file and return its contents."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def collect_strings_from_files(file_list):
    """
    Collect positive strings from a list of feature JSON files.

    Parameters
    ----------
    file_list : list
        List of file paths to `logits_and_description_<query>.json`.

    Returns
    -------
    dict
        Dictionary with key "positive_strings" mapping to a list of entries, 
        each containing string, index, query, filename, and description.
    """
    collected_data = {"positive_strings": []}
    for filename in file_list:
        data = load_json_file(filename)
        query = filename.split('\\')[2]  # assumes query is the 3rd folder in path

        if isinstance(data, list):
            for entry in data:
                if not isinstance(entry, dict):
                    continue
                index = entry.get('index')
                description = entry.get('description', 'No description available')
                for pos_str in entry.get('positive_strings', []):
                    collected_data["positive_strings"].append({
                        "string": pos_str,
                        "index": index,
                        "query": query,
                        "filename": filename,
                        "description": description
                    })
        else:
            print(f"Warning: {filename} does not contain a list of entries.")
    return collected_data


def count_duplicates(input_data, directory):
    """
    Count how many times each positive string appears.

    Parameters
    ----------
    input_data : dict
        Collected positive strings.
    directory : str
        Directory where results will be written.

    Saves
    -----
    - `duplicates_pos_count.json` with string → count
    """
    positive_strings = [entry['string'] for entry in input_data['positive_strings']]
    positive_counts = Counter(positive_strings)

    duplicates = {
        "positive_strings": {string: count for string, count in positive_counts.items() if count > 1}
    }

    with open(os.path.join(directory, 'duplicates_pos_count.json'), 'w') as json_file:
        json.dump(duplicates, json_file, indent=4)

    print("Positive string duplicate analysis written to duplicates_pos_count.json")


def retrieve_and_save_duplicates(duplicates_file, collected_data, output_file):
    """
    Collect detailed metadata for duplicate positive strings.

    Parameters
    ----------
    duplicates_file : str
        Path to JSON file with duplicate counts.
    collected_data : dict
        Positive strings collected from all queries.
    output_file : str
        Output JSON file path.

    Saves
    -----
    - JSON mapping each duplicate string → list of {query, index}.
    """
    with open(duplicates_file, 'r') as df:
        duplicates_count = json.load(df)

    collected_strings = collected_data["positive_strings"]
    duplicates_info = {}

    for key, count in duplicates_count["positive_strings"].items():
        if count > 1:
            duplicates_info[key] = [
                {"query": entry.get("query"), "index": entry.get("index")}
                for entry in collected_strings if key in entry.get("string", "")
            ]

    with open(output_file, 'w') as of:
        json.dump(duplicates_info, of, indent=4)

    print(f"Duplicate information saved to {output_file}")


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def analyze_positive_logits(directory='json'):
    """
    Run duplicate analysis for positive strings.

    Parameters
    ----------
    directory : str
        Root directory containing per-query JSONs.

    Process
    -------
    - Collect positive strings across all queries
    - Count duplicates
    - Save count and metadata results
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith('logits_and_description') and file.endswith('.json'):
                file_list.append(os.path.join(root, file))

    collected_data = collect_strings_from_files(file_list)
    count_duplicates(collected_data, directory)
    retrieve_and_save_duplicates(
        os.path.join(directory, 'duplicates_pos_count.json'),
        collected_data,
        os.path.join(directory, 'duplicates_pos_info.json')
    )


if __name__ == "__main__":
    analyze_positive_logits(directory="json6")
