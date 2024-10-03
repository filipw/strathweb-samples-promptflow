import os
import json

def load_metadata(metadata_path):
    try:
        with open(metadata_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load metadata from {metadata_path}: {e}")
        return None

def save_individual_metadata(item, output_folder):
    try:
        filename = os.path.splitext(item['image_blob_path'])[0] + '.json'
        output_path = os.path.join(output_folder, filename)

        with open(output_path, 'w') as file:
            json.dump(item, file, indent=4)
        
        print(f"Metadata saved to {output_path}")
    except Exception as e:
        print(f"Failed to save individual metadata file: {e}")

def split_metadata_to_individual_files(metadata_path, output_folder):
    metadata = load_metadata(metadata_path)

    if metadata is None:
        print("Metadata loading failed. Exiting process.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for item in metadata:
        if 'image_blob_path' in item:
            save_individual_metadata(item, output_folder)

folder_path = "../rag-chat/data"
metadata_path = os.path.join(folder_path, 'metadata_structured.json')
output_folder = os.path.join(folder_path, 'processed_data')
split_metadata_to_individual_files(metadata_path, output_folder)