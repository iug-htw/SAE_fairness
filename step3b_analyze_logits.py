
import json
import os
from collections import defaultdict

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
                for pos_str in entry.get('positive_strings', []):
                    collected_data["positive_strings"].append({
                        "string": pos_str,
                        "index": index,
                        "query": query
                    })
                for neg_str in entry.get('negative_strings', []):
                    collected_data["negative_strings"].append({
                        "string": neg_str,
                        "index": index,
                        "query": query
                    })
        else:
            print(f"Warning: {filename} does not contain a list of entries.")
    return collected_data

def main(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_list.append(os.path.join(root, file))
    print("Files found:", file_list)
    collected_data = collect_strings_from_files(file_list)
    
    with open(directory+'collected_strings.json', 'w') as outfile:
        json.dump(collected_data, outfile, indent=4)
    
    print("Results written to collected_strings.json")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python collect_strings.py <directory>")
    else:
        main(sys.argv[1])

