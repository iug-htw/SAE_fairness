import json
import csv
import os
import pandas as pd
import re

# Define the base folder containing the model subfolders
base_folder = 'json5/'

# Define crime-related keywords for analysis
crime_keywords = ["terrorism", "terrorist", "crime", "criminal", "violence", "extremist", "extremism", "attack", "radical", "assault", "shooting", "bomb"]
queries_to_analyze = ["christianity", "islam", "judaism" , "buddhism", "hinduism"]	

# Function to clean text by removing non-printable characters and extra spaces
def clean_text(text):
    text = re.sub(r'[^\x20-\x7E]', ' ', text)  # Remove non-printable characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()

def _activation_analysis_keyword(base_folder="json", query="christianity", topic='crime', keywords=crime_keywords):
    # Initialize a list to store the summary data
    summary_data = []
    
    # Define the output CSV file path
    output_csv_path = f'{base_folder}/{topic}_mentions_summary_{query}.csv'
    print(output_csv_path)

    # Iterate through all model subfolders in the base folder
    for model_folder in os.listdir(base_folder):
        model_folder_path = os.path.join(base_folder, model_folder)
        if os.path.isdir(model_folder_path):
            # Iterate through all subfolders in the model folder
            for source_folder in os.listdir(model_folder_path):
                source_folder_path = os.path.join(model_folder_path, source_folder)
                if os.path.isdir(source_folder_path):
                    csv_file_path = os.path.join(source_folder_path, f'activation_analysis_{query}.csv')
                    # Load the file while accounting for potential issues in the format
                    try:
                        activation_data = pd.read_csv(csv_file_path, engine='python', encoding='utf-8', quotechar='"', sep=',')
                        # Check if the CSV file is empty
                        if activation_data.empty:
                            print(f"{csv_file_path} is empty. Skipping to the next folder.")
                            continue
                        # Display the first few rows to confirm successful loading
                        #print(religion_activations_data.head())
                    except Exception as e:
                        print(f"Error loading {csv_file_path}: {e}")
                        continue
                    
                    # Check if 'activation_tokens' column exists
                    if 'activation_tokens' not in activation_data.columns:
                        print(f"'activation_tokens' column not found in {csv_file_path}")
                        continue

                    # Add a column indicating whether related keywords are mentioned in the activation tokens
                    activation_data[f"{topic} Mentions"] = activation_data["activation_tokens"].apply(
                        lambda text: any(keyword in text.lower() for keyword in keywords)
                    )
                    
                    # Check if 'query_term' column exists
                    if 'query_term' not in activation_data.columns:
                        print(f"'query_term' column not found in {csv_file_path}")
                        continue

                    # Extract unique examples of activation tokens mentioning related keywords
                    unique_topic_mentions = activation_data[activation_data[f"{topic} Mentions"]]["activation_tokens"].drop_duplicates()

                    # Summarize the findings
                    total_queries = len(activation_data)
                    topic_mentions_count = activation_data[f"{topic} Mentions"].sum()
                    queries_with_topic_mentions = activation_data[activation_data[f"{topic} Mentions"]]["query_term"].unique()
                    summary_data.append({
                        "model": f"{model_folder}/{source_folder}",
                        "total_queries": total_queries,
                        f"{topic}_mentions_count": topic_mentions_count,
                        f"queries_with_{topic}_mentions": ', '.join(queries_with_topic_mentions),
                        "examples": [clean_text(example) for example in unique_topic_mentions.head(5).tolist()] # Clean text
                    })
        

    # Write the summary data to a CSV file
    with open(output_csv_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["model", "total_queries", f"{topic}_mentions_count", f"queries_with_{topic}_mentions", "example"])
        writer.writeheader()
        for row in summary_data:
            for example in row["examples"]:
                writer.writerow({
                    "model": row["model"],
                    "total_queries": row["total_queries"],
                    f"{topic}_mentions_count": row[f"{topic}_mentions_count"],
                    f"queries_with_{topic}_mentions": row[f"queries_with_{topic}_mentions"],
                    "example": example
                })


def activation_analysis_keyword(base_folder="json", groups=queries_to_analyze, topic='crime', keywords=crime_keywords):
    for group in groups:
        _activation_analysis_keyword(base_folder=base_folder, query=group, topic=topic, keywords=keywords)

if __name__ == "__main__":
    activation_analysis_keyword(base_folder)