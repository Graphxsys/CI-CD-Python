import os
import requests
import json

def get_username():
    """Retrieve the username for both Windows and macOS/Linux."""
    return os.getenv("USERNAME") or os.getenv("USER")

def deploy_repo(server_url, repo_url, branch="main", commit_hash=None, local_dir="./test", exclude_ext=".ipynb"):
    payload = {
        "username": get_username(),
        "repo_url": repo_url,
        "branch": branch,
        "commit_hash": commit_hash,
        "local_dir": local_dir,
        "exclude_ext": exclude_ext,
    }
    
    try:
        response = requests.post(f"{server_url}/deploy", json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            print("Deployment successful!")
        else:
            print("Deployment failed!")
        
        print(json.dumps(response_data, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    server_url = "http://127.0.0.1:9000/"  # Change to your Flask server URL
    repo_url = "https://github.com/SinkuKumar/CI-CD-Python.git"
    commit_hash = "72a3eb3f83fc6f148d343f869070f067c44b4d4e"
    local_dir = "./Users/Sinku/Desktop/Deployment"
    deploy_repo(server_url=server_url, repo_url=repo_url, commit_hash=commit_hash, local_dir=local_dir)