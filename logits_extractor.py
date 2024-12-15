import json
import os

queries=["muslim", "islam","terrorist","christian","christianity"]


def extract_logits(feature,query):
    layer, index = feature
    filename = 'json/'+query+'/data_for_feature_' + str(index) + '.json'
    # Load the JSON data from a file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract the neg_str and pos_str values
    neg_str = data.get('neg_str', [])
    pos_str = data.get('pos_str', [])

    # Extract the layer and description from the explanations
    explanations = data.get('explanations', [])
    if explanations:
        layer = explanations[0].get('layer')
        description = explanations[0].get('description')
    else:
        print("No explanations found.")
    
    # Structure the output data
    output_data = {
        "index": index,
        "layer": layer,
        "url": filename,
        "negative_strings": neg_str,
        "positive_strings": pos_str,
        "description": description
    }
    
    # Save the output data to a JSON file
    output_filename2 = f'json/output_{os.path.basename(filename)}'
    with open(output_filename, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

    print(f"Output saved to {output_filename}")
    return output_data

# Main execution
for query in queries:
    all_output_data = []  # List to collect all output data
    output_filename = 'json/'+query+'/logits_and_description_'+str(query)+'.json'
    # Read the JSON file
    filename = f'json/{query}/explanation_for_query_{query}.json'
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")

    with open(filename, 'r') as json_file:
        response_data = json.load(json_file)

    # Extract the featureId from the response
    features = []
    for result in response_data.get('results', []):
        layer = result.get('layer')
        index = result.get('index')
        features.append((layer, index))

    print(features)
    if features:
        for feature in features:
            output_data = extract_logits(feature,query)
            if output_data:
                all_output_data.append(output_data)
            # Save all collected output data to a single JSON file
    else:
        print("Feature IDs not found in the response.")
    
    with open(output_filename, 'w') as output_file:
        json.dump(all_output_data, output_file, indent=4)
    print(f"All output data saved to {output_filename}")    