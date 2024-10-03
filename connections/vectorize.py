import os
import json
import requests

def load_metadata(metadata_path):
    with open(metadata_path, 'r') as file:
        return json.load(file)

def save_metadata(metadata, metadata_path):
    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)

def vectorize_image(image_path, endpoint, subscription_key):
    api_url = f"{endpoint}/computervision/retrieval:vectorizeImage?api-version=2024-02-01&model-version=2023-04-15"
    
    with open(image_path, 'rb') as file:
        image_data = file.read()

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    response = requests.post(api_url, headers=headers, data=image_data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

def process_metadata_for_image_vectors(metadata_path, folder_path, endpoint, subscription_key):
    metadata = load_metadata(os.path.join(folder_path, metadata_path))

    for item in metadata:
        image_blob_path = item.get('image_blob_path')
        if image_blob_path:
            image_path = os.path.join(folder_path, image_blob_path)
            if os.path.exists(image_path):
                if 'image_vector' not in item:
                    try:
                        vector_data = vectorize_image(image_path, endpoint, subscription_key)

                        item['image_vector'] = vector_data['vector']
                        print(f"Image vector added for {image_blob_path}")

                    except Exception as e:
                        print(f"Failed to vectorize {image_blob_path}: {e}")
                else:
                    print(f"Image vector already exists for {image_blob_path}")
            else:
                print(f"Image not found: {image_path}")

    save_metadata(metadata, os.path.join(folder_path, metadata_path))
    print("Metadata has been updated with image vectors.")


AZURE_VISION_ENDPOINT = os.environ["AZURE_VISION_ENDPOINT"]
AZURE_VISION_KEY = os.environ["AZURE_VISION_KEY"]

process_metadata_for_image_vectors("metadata_structured.json", "../rag-chat/data", AZURE_VISION_ENDPOINT, AZURE_VISION_KEY)