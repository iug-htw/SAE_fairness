import json
import csv
import os
import pandas as pd
import re

# Define the base folder containing the model subfolders
base_folder = 'json/'

# Define crime-related keywords for analysis
crime_keywords = ["terrorism", "terrorist", "crime", "criminal", "violence", "extremism", "attack"]

# Define the output CSV file path
output_csv_path = 'crime_mentions_summary_judaism.csv'

# Initialize a list to store the summary data
summary_data = []

# Function to clean text by removing non-printable characters and extra spaces
def clean_text(text):
    text = re.sub(r'[^\x20-\x7E]', ' ', text)  # Remove non-printable characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()

for model_folder in os.listdir(base_folder):
    model_folder_path = os.path.join(base_folder, model_folder)
    if os.path.isdir(model_folder_path):
        csv_file_path = os.path.join(model_folder_path, 'activation_analysis_judaism.csv')
        # Load the file while accounting for potential issues in the format
        print(csv_file_path)
        try:
            islam_activations_data = pd.read_csv(csv_file_path, engine='python', encoding='utf-8', quotechar='"', sep=',')
            # Check if the CSV file is empty
            if islam_activations_data.empty:
                print(f"{csv_file_path} is empty. Skipping to the next folder.")
                continue
            # Display the first few rows to confirm successful loading
            #print(islam_activations_data.head())
        except Exception as e:
            print(f"Error loading {csv_file_path}: {e}")
            continue
        
        # Check if 'activation_tokens' column exists
        if 'activation_tokens' not in islam_activations_data.columns:
            print(f"'activation_tokens' column not found in {csv_file_path}")
            continue

        # Add a column indicating whether crime-related keywords are mentioned in the activation tokens
        islam_activations_data["Crime Mentions"] = islam_activations_data["activation_tokens"].apply(
            lambda text: any(keyword in text.lower() for keyword in crime_keywords)
        )
        
        # Check if 'query_term' column exists
        if 'query_term' not in islam_activations_data.columns:
            print(f"'query_term' column not found in {csv_file_path}")
            continue

        # Extract unique examples of activation tokens mentioning crime-related keywords
        unique_crime_mentions = islam_activations_data[islam_activations_data["Crime Mentions"]]["activation_tokens"].drop_duplicates()

        # Summarize the findings
        total_queries = len(islam_activations_data)
        crime_mentions_count = islam_activations_data["Crime Mentions"].sum()
        queries_with_crime_mentions = islam_activations_data[islam_activations_data["Crime Mentions"]]["query_term"].unique()
        summary_data.append({
            "model": model_folder,
            "total_queries": total_queries,
            "crime_mentions_count": crime_mentions_count,
            "queries_with_crime_mentions": ', '.join(queries_with_crime_mentions),
            "examples": [clean_text(example) for example in unique_crime_mentions.head(5).tolist()] # Clean text
        })
    

# Write the summary data to a CSV file
with open(output_csv_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["model", "total_queries", "crime_mentions_count", "queries_with_crime_mentions", "example"])
    writer.writeheader()
    for row in summary_data:
        for example in row["examples"]:
            writer.writerow({
                "model": row["model"],
                "total_queries": row["total_queries"],
                "crime_mentions_count": row["crime_mentions_count"],
                "queries_with_crime_mentions": row["queries_with_crime_mentions"],
                "example": example
            })
