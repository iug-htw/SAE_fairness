import os
import csv

def combine_csv_files(model_source_sets, output_path):
    combined_data = {}
    
    for model, source in model_source_sets:
        input_path = f'json4/{model}/{source}/common_features.csv'
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
    
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Term1', 'Term2', 'Term3'] + [f'{model}-{source}' for model, source in model_source_sets]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for term_pair, features in combined_data.items():
            row = {'Term1': term_pair[0], 'Term2': term_pair[1], 'Term3': term_pair[2]}
            for model, source in model_source_sets:
                row[f'{model}-{source}'] = features.get(f'{model}-{source}', 0)
            writer.writerow(row)

if __name__ == "__main__":
    model_source_sets = [
        ("gpt2-small", "res-jb"),#fertig
        ("gpt2-small", "att-kk"), #fertig
        #("gpt2-small", "att_32k-oai"), #bis programmer
        #("gpt2-small", "mlp_32k-oai"),bis programmer
        ("gemma-2-2b", "gemmascope-att-16k"),# fertig
        ("gemma-2-2b", "gemmascope-att-65k"),# fertig
        ("gemma-2-2b", "gemmascope-mlp-16k"),# fertig
        #("gemma-2-2b", "gemmascope-mlp-65k"), überspringen!
        #("gemma-2-2b", "gemmascope-res-16k"), überspringen!
        #("gemma-2-2b", "gemmascope-res-65k"), überspringen!
        #("gemma-2-9b", "gemmascope-res-16k"), überspringen!
        #("gemma-2-9b-it", "gemmascope-res-16k"), überspringen!
        ("gemma-2-9b-it", "gemmascope-res-131k"),  # fertig
        ("llama3.1-8b","llamascope-res-32k"),# fertig
    ]
    output_path = 'json4/combined_common_features.csv'
    combine_csv_files(model_source_sets, output_path)
    print(f"Combined CSV saved to {output_path}")
