import base64
import requests
import os
import json
from config import *

def fetch_data_from_db():
    """
    Fetch the data using the API with 'raw' headers.
    This bypasses the 1MB limit and uses your token for high rate limits.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"
    
    # Header 1: Your Token for permission/rate-limiting
    # Header 2: 'vnd.github.v3.raw' tells GitHub "Just give me the text, not the JSON metadata"
    headers = {
        "Authorization": f"token {GIT_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        decoded_content = response.text  # This will be your full 1MB+ text
        
        # We still need the SHA for updating the file later
        # So we make a quick second call WITHOUT the 'raw' header to get metadata
        meta_headers = {"Authorization": f"token {GIT_TOKEN}"}
        meta_response = requests.get(url, headers=meta_headers)
        sha = meta_response.json().get('sha') if meta_response.status_code == 200 else None
        
        return decoded_content, sha
    else:
        print(f"Error fetching data: {response.status_code}")
        return "", None

def update_data_in_db(new_json_data):
    """
    Overwrite the existing content of the anime_data.txt file in the GitHub repository with new JSON data.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"
    headers = {
        "Authorization": f"token {GIT_TOKEN}"
    }

    # Step 1: Fetch the current file metadata (to get the 'sha')
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        sha = data.get('sha', None)  # Fetch the current sha

    else:
        print("Error fetching the existing file:", response.json())
        return False

    # Step 2: Validate and sort the new data
    try:
        anime_list = json.loads(new_json_data)  # Ensure new data is valid JSON
        if not isinstance(anime_list, list):
            print("Error: Data should be a list of anime entries.")
            return False
        # Sort the data by `aid` in ascending order
        anime_list_sorted = sorted(anime_list, key=lambda x: x.get('aid', 0))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        return False

    # Step 3: Convert the sorted list back to JSON string
    sorted_json_data = json.dumps(anime_list_sorted, indent=4)

    # Step 4: Base64 encode the sorted content
    encoded_data = base64.b64encode(sorted_json_data.encode("utf-8")).decode("utf-8")

    # Step 5: Prepare the payload to overwrite the file
    update_payload = {
        "message": "♦️ DONE UPDATING ♦️",
        "sha": sha,  # Use the current sha to update the file
        "content": encoded_data  # Base64 encoded sorted content
    }

    # Step 6: Send the PUT request to update the file
    response = requests.put(url, headers=headers, json=update_payload)

    if response.status_code == 200:
        print("Successfully Updated the Database.")
        return True
    else:
        print("Error updating the Database:", response.json())
        return False
