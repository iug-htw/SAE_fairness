
import json
import os
from collections import defaultdict, Counter

def load_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def collect_strings_from_files(file_list):
    collected_data = {
        "positive_strings": [],
        "negative_strings": []
    }
    for filename in file_list:
        data = load_json_file(filename)
        query = filename.split('/')[2] #query is the subfolder name of filename
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
                for neg_str in entry.get('negative_strings', []):
                    collected_data["negative_strings"].append({
                        "string": neg_str,
                        "index": index,
                        "query": query,
                        "filename": filename,
                        "description": description   
                    })
        else:
            print(f"Warning: {filename} does not contain a list of entries.")
    return collected_data

def analyze_duplicates(input_file, output_file):
    data = load_json_file(input_file)
    positive_strings = [entry['string'] for entry in data['positive_strings']]
    negative_strings = [entry['string'] for entry in data['negative_strings']]
        
    positive_counts = Counter(positive_strings)
    negative_counts = Counter(negative_strings)
    

    duplicates = {
        "positive_strings": {string: count for string, count in positive_counts.items() if count > 1},
        "negative_strings": {string: count for string, count in negative_counts.items() if count > 1}
    }
        
    with open(output_file, 'w') as outfile:
        json.dump(duplicates, outfile, indent=4)
        
    print(f"Duplicate analysis written to {output_file}")

def retrieve_and_save_duplicates(duplicates_file, collected_data, output_file):
    with open(duplicates_file, 'r') as df:
        duplicates_count = json.load(df)
    
    #with open(collected_file, 'r') as cf:
    #    collected_strings = json.load(cf)
    collected_strings = collected_data["positive_strings"]

    duplicates_info = {}
    
    for key, count in duplicates_count["positive_strings"].items():
        if count > 1:
            duplicates_info[key] = []
            for entry in collected_strings:
                print(f"Checking entry: {entry}")  # Debug print
                #if key in entry.get("string", ""):
                #    print(f"Match found for key: {key}")  # Debug print
                #    duplicates_info[key].append({
                #       "query": entry.get("query"),
                #        "index": entry.get("index")
                #    })
    
    with open(output_file, 'w') as of:
        json.dump(duplicates_info, of, indent=4)
    
    print(f"Duplicate information saved to {output_file}")

def main(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith('logits_and_description') and file.endswith('.json'):
                file_list.append(os.path.join(root, file))
    print("Files found:", file_list)
    collected_data = collect_strings_from_files(file_list)
    

    #doppelte positive/negative strings finden und zählen
    analyze_duplicates(directory+'collected_strings.json', directory+'duplicates_count.json')
    #für diese doppelten strings die query und index finden
    retrieve_and_save_duplicates(directory+'duplicates_count.json', collected_data, directory+'duplicates_info.json')   

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python collect_strings.py <directory> Directory should be folder for one model")
    else:
        main(sys.argv[1])

