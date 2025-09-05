"""
step6_activation_keyword_analysis.py

This script implements Step 6 of the analysis pipeline for:
"Mechanistic Interpretability with SAEs: Probing Religion, Violence, and Geography in Large Language Models"
(AEQUITAS Workshop @ ECAI 2025).

Purpose
-------
Search the **activation tokens** (extracted in Step 5) for crime-related keywords, 
in order to quantify how often violent associations appear within the activation contexts 
of religion-related features.

Workflow
--------
1. For each religion group (Christianity, Islam, Judaism, Buddhism, Hinduism):
   - Load `activation_analysis_<religion>.csv` produced in Step 5 for each model/source.
   - Check if any activation tokens contain crime-related keywords.
   - Count total queries vs. those mentioning crime terms.
   - Collect unique examples of matched activations.

2. Summarize results per (model, source):
   - Number of total queries inspected
   - Number of crime mentions
   - Which query terms contained crime mentions
   - Example activation texts (cleaned)

3. Save results to `<base_folder>/crime_mentions_summary_<religion>.csv`.

Notes
-----
- The analysis can be adapted to other keyword categories (e.g., geography, poverty, wealth)
  by changing `topic` and `keywords`.
"""

import csv
import os
import pandas as pd
import re

# Define crime-related keywords for analysis
crime_keywords = [
    "terrorism", "terrorist", "crime", "criminal", "violence",
    "extremist", "extremism", "attack", "radical", "assault",
    "shooting", "bomb"
]

# Religion groups to analyze
queries_to_analyze = ["christianity", "islam", "judaism", "buddhism", "hinduism"]


# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

def clean_text(text):
    """ Clean activation text by removing non-printable characters and extra spaces. """
    text = re.sub(r'[^\x20-\x7E]', ' ', text)  # Remove non-printable characters
    text = re.sub(r'\s+', ' ', text)           # Replace multiple spaces with one
    return text.strip()

def _activation_analysis_keyword(base_folder="json", query="christianity", topic='crime', keywords=crime_keywords):
    """
    Run keyword analysis for a single religion group.

    Parameters
    ----------
    base_folder : str
        Root directory containing activation CSVs from Step 5.
    query : str
        Religion group to analyze (e.g., "islam").
    topic : str
        Analysis category (default = "crime").
    keywords : list of str
        Keywords to search for in activation tokens.

    Output
    ------
    A summary CSV file saved as:
        `<base_folder>/<topic>_mentions_summary_<query>.csv`
    """
    summary_data = []  # Holds results for all models/sources

    # Define output CSV path for this religion group
    output_csv_path = f'{base_folder}/{topic}_mentions_summary_{query}.csv'
    print(output_csv_path)

    # Iterate through model folders
    for model_folder in os.listdir(base_folder):
        model_folder_path = os.path.join(base_folder, model_folder)
        if os.path.isdir(model_folder_path):

            # Iterate through source folders (e.g., res-16k, att-16k)
            for source_folder in os.listdir(model_folder_path):
                source_folder_path = os.path.join(model_folder_path, source_folder)
                if os.path.isdir(source_folder_path):

                    # Path to activation CSV for this religion group
                    csv_file_path = os.path.join(source_folder_path, f'activation_analysis_{query}.csv')

                    try:
                        # Load CSV safely
                        activation_data = pd.read_csv(csv_file_path, engine='python',
                                                      encoding='utf-8', quotechar='"', sep=',')
                        if activation_data.empty:
                            print(f"{csv_file_path} is empty. Skipping to the next folder.")
                            continue
                    except Exception as e:
                        print(f"Error loading {csv_file_path}: {e}")
                        continue

                    # Ensure required columns exist
                    if 'activation_tokens' not in activation_data.columns:
                        print(f"'activation_tokens' column not found in {csv_file_path}")
                        continue
                    if 'query_term' not in activation_data.columns:
                        print(f"'query_term' column not found in {csv_file_path}")
                        continue

                    # Flag rows containing the keywords
                    activation_data[f"{topic} Mentions"] = activation_data["activation_tokens"].apply(
                        lambda text: any(keyword in str(text).lower() for keyword in keywords)
                    )

                    # Extract unique examples where keywords occurred
                    unique_topic_mentions = activation_data[
                        activation_data[f"{topic} Mentions"]
                    ]["activation_tokens"].drop_duplicates()

                    # Summarize results for this model/source
                    total_queries = len(activation_data)
                    topic_mentions_count = activation_data[f"{topic} Mentions"].sum()
                    queries_with_topic_mentions = activation_data[
                        activation_data[f"{topic} Mentions"]
                    ]["query_term"].unique()

                    summary_data.append({
                        "model": f"{model_folder}/{source_folder}",
                        "total_queries": total_queries,
                        f"{topic}_mentions_count": topic_mentions_count,
                        f"queries_with_{topic}_mentions": ', '.join(queries_with_topic_mentions),
                        "examples": [
                            clean_text(example) for example in unique_topic_mentions.head(5).tolist()
                        ]
                    })

    # Save summary results to CSV
    with open(output_csv_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["model", "total_queries", f"{topic}_mentions_count",
                        f"queries_with_{topic}_mentions", "example"]
        )
        writer.writeheader()

        # Write multiple rows if multiple examples exist for a model/source
        for row in summary_data:
            for example in row["examples"]:
                writer.writerow({
                    "model": row["model"],
                    "total_queries": row["total_queries"],
                    f"{topic}_mentions_count": row[f"{topic}_mentions_count"],
                    f"queries_with_{topic}_mentions": row[f"queries_with_{topic}_mentions"],
                    "example": example
                })


# --------------------------------------------------------------------
# Main execution
# --------------------------------------------------------------------

def activation_analysis_keyword(base_folder="json", groups=queries_to_analyze,
                                topic='crime', keywords=crime_keywords):
    """
    Run keyword analysis for multiple religion groups.

    Parameters
    ----------
    base_folder : str
        Root directory containing activation CSVs.
    groups : list of str
        Religion groups to analyze (default = all five).
    topic : str
        Category of analysis (default = "crime").
    keywords : list of str
        Keywords to detect in activation tokens.
    """
    
    for group in groups:
        _activation_analysis_keyword(base_folder=base_folder, query=group,
                                     topic=topic, keywords=keywords)


if __name__ == "__main__":
    activation_analysis_keyword(base_folder="json7")
