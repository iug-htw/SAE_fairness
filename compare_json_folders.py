import os
import csv

# Define the base folders to compare
folder1 = 'json'
folder2 = 'json3'

# Function to get all file paths in a folder and its subfolders
def get_all_file_paths(base_folder):
    file_paths = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            file_paths.append(os.path.relpath(os.path.join(root, file), base_folder))
    return set(file_paths)

# Get all file paths in both folders
folder1_files = get_all_file_paths(folder1)
folder2_files = get_all_file_paths(folder2)

# Find files that only exist in one of the folders
only_in_folder1 = folder1_files - folder2_files
only_in_folder2 = folder2_files - folder1_files

# Find files that exist in both folders
in_both_folders = folder1_files & folder2_files

# Define the output CSV file path
output_csv_path = 'comparison_results.csv'

# Write the results to a CSV file
with open(output_csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['File Path', 'Location'])
    
    for file in sorted(only_in_folder1):
        writer.writerow([os.path.join(folder1, file), 'Only in folder1 (json)'])
    
    for file in sorted(only_in_folder2):
        writer.writerow([os.path.join(folder2, file), 'Only in folder2 (json3)'])
    
    for file in sorted(in_both_folders):
        writer.writerow([os.path.join(folder1, file), 'In both folders'])

print(f"Comparison results written to {output_csv_path}")
