import json
from collections import defaultdict

#This checks for duplicate positive and negative strings in the logit data    
# currently only look into one file
#next step is to look into all files and compare across files
#should also output table with all the duplicates, possibly in json format


def load_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def find_redundancies(data):
    positive_strings = defaultdict(list)
    negative_strings = defaultdict(list)

    for entry in data:
        index = entry['index']
        for pos_str in entry.get('positive_strings', []):
            positive_strings[pos_str].append(index)
        for neg_str in entry.get('negative_strings', []):
            negative_strings[neg_str].append(index)

    redundant_positive = {k: v for k, v in positive_strings.items() if len(v) > 1}
    redundant_negative = {k: v for k, v in negative_strings.items() if len(v) > 1}

    return redundant_positive, redundant_negative

def main():
    filename = 'json/christian/logits_and_description_christian.json'
    data = load_json_file(filename)
    redundant_positive, redundant_negative = find_redundancies(data)

    if redundant_positive:
        print("Redundant positive strings found:")
        for pos_str, indices in redundant_positive.items():
            print(f"'{pos_str}' found in indices: {', '.join(indices)}")
    else:
        print("No redundant positive strings found.")

    if redundant_negative:
        print("Redundant negative strings found:")
        for neg_str, indices in redundant_negative.items():
            print(f"'{neg_str}' found in indices: {', '.join(indices)}")
    else:
        print("No redundant negative strings found.")

if __name__ == "__main__":
    main()