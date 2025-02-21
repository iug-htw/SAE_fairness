import json
import os

def load_queries(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []


def extract_logits(feature, modelRelease, residual_stream, query, output_dir = 'json'):
    layer, index = feature
    filename = os.path.join(output_dir, modelRelease, residual_stream, query, 'data_for_feature_' + str(index) + '.json')
    # Load the JSON data from a file
    if not os.path.exists(filename):
        print(f"File {filename} does not exist. Skipping...")
    else:
        with open(filename, 'r') as file:
            data = json.load(file)

        # Extract the neg_str and pos_str values
        neg_str = data.get('neg_str', [])
        pos_str = data.get('pos_str', [])

        # Extract the layer and description from the explanations
        explanations = data.get('explanations', [])
        layer = ""
        description = ""
        if explanations:
            layer = explanations[0].get('layer')
            description = explanations[0].get('description')
        else:
            print(f"❗No explanations found. [{modelRelease}-{residual_stream}-{query}]")
        
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
        output_filename2 = os.path.join(output_dir, modelRelease, residual_stream, query, f'output_{os.path.basename(filename)}')
        with open(output_filename2, 'w') as output_file:
            json.dump(output_data, output_file, indent=4)

        # print(f"Output saved to {output_filename2}")
        return output_data

# Main execution

def extract_logits_for_all_queries(modelReleases, queries_file='queries.json', main_dir='json'):
    queries = load_queries(filename=queries_file)

    for modelRelease in modelReleases:
        # list out all files in the main_dir/modelRelease/query/
        files = os.listdir(os.path.join(main_dir, modelRelease))

        for residual_stream in files:
            for query in queries:
                all_output_data = []  # List to collect all output data
                output_filename = os.path.join(main_dir, modelRelease, residual_stream, query, 'logits_and_description_'+str(query)+'.json')
            
                # Read the JSON file
                input_filename = os.path.join(main_dir, modelRelease, residual_stream, query, 'explanation_for_query_'+query+'.json')

                if not os.path.exists(input_filename):
                    print(f"File {input_filename} does not exist.")

                with open(input_filename, 'r') as json_file:
                    response_data = json.load(json_file)

                # Extract the featureId from the response
                features = []
                for result in response_data.get('result', []):
                    layer = result.get('layer')
                    index = result.get('index')
                    features.append((layer, index))
                    
                if features:
                    for feature in features:
                        output_data = extract_logits(feature, modelRelease, residual_stream, query, output_dir=main_dir)
                        if output_data:
                            all_output_data.append(output_data)
                        # Save all collected output data to a single JSON file
                else:
                    print("Feature IDs not found in the response.")
                
                with open(output_filename, 'w') as output_file:
                    json.dump(all_output_data, output_file, indent=4)
                print(f"✅ {query} => {modelRelease}-{residual_stream}")    



if __name__ == "__main__":
    modelReleases = [
        "gemma-2-2b",
        "gemma-2-9b",
        "gemma-2-9b-it",
        "gpt2-small",
        "llama3.1-8b",
    ]

    extract_logits_for_all_queries(modelReleases, queries_file='queries6.json', main_dir='json6')