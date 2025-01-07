import os
import csv

def combine_csv_files(model_releases, output_path):
    combined_data = {}
    
    for model_release in model_releases:
        input_path = f'/workspaces/SAE_fairness/json/{model_release}/common_features.csv'
        if os.path.exists(input_path):
            with open(input_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    term_pair = (row['Term1'], row['Term2'], row['Term3'])
                    if term_pair not in combined_data:
                        combined_data[term_pair] = {}
                    combined_data[term_pair][model_release] = row['CommonFeatures']
        else:
            print(f"File {input_path} does not exist.")
    
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Term1', 'Term2', 'Term3'] + model_releases
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for term_pair, features in combined_data.items():
            row = {'Term1': term_pair[0], 'Term2': term_pair[1], 'Term3': term_pair[2]}
            for model_release in model_releases:
                row[model_release] = features.get(model_release, 0)
            writer.writerow(row)

if __name__ == "__main__":
    model_releases = ["llama3.1-8b-eleuther_gp", "llama-scope", "gemma-scope", "gpt2sm-apollojt", "gpt2sm-rfs-jb", "gpt2sm-kk", "llama3-8b-it-res-jh"]
    output_path = '/workspaces/SAE_fairness/json/combined_common_features.csv'
    combine_csv_files(model_releases, output_path)
    print(f"Combined CSV saved to {output_path}")
