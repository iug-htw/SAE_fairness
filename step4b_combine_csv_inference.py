import os
import csv

def combine_csv_files(model_sources, main_dir="json"):
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
