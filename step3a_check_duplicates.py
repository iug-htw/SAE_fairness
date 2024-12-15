import os
import re
from collections import defaultdict

def find_feature_numbers(directory):
    feature_pattern = re.compile(r'data_for_feature_(\d+)\.json')
    feature_files = defaultdict(list)

    for root, _, files in os.walk(directory):
        for file in files:
            match = feature_pattern.search(file)
            if match:
                feature_number = match.group(1)
                feature_files[feature_number].append(os.path.join(root, file))

    return feature_files
def check_for_duplicates(feature_files):
    duplicates = {k: v for k, v in feature_files.items() if len(v) > 1}
    return duplicates

def main():
    directory = 'json'
    feature_files = find_feature_numbers(directory)
    duplicates = check_for_duplicates(feature_files)

    if duplicates:
        print("Duplicate feature numbers found:")
        for feature_number, files in duplicates.items():
            print(f"Feature number {feature_number} found in files:")
            for file in files:
                print(f"  - {file}")
    else:
        print("No duplicate feature numbers found.")

if __name__ == "__main__":
    main()