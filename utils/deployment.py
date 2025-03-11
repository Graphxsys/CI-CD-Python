import os
import json
import subprocess

import requests
import yaml


def get_username():
    """Retrieve the username for both Windows and macOS/Linux."""
    return os.getenv("USERNAME") or os.getenv("USER")

def load_config(config_path="deployment.yaml"):
    """Load deployment configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def deploy_repo(username, server_url, repo_url, branch="main", commit_hash=None, local_dir="./test", exclude_ext=".ipynb"):
    """Deploy the repository using the provided parameters."""
    payload = {
        "username": username,
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

def execute_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip() if e.stderr else str(e)}

def clone_or_update_repo(repo_url, branch, commit_hash, local_dir, logs):
    if not os.path.exists(local_dir):
        logs.append(f"Cloning repository {repo_url} into {local_dir}")
        response = execute_command(["git", "clone", "-b", branch, repo_url, local_dir])
    else:
        logs.append("Repository already exists. Fetching latest changes.")
        response = execute_command(["git", "-C", local_dir, "fetch"])
    
    if not response["success"]:
        return response

    if commit_hash:
        logs.append(f"Checking out specific commit {commit_hash}")
        response = execute_command(["git", "-C", local_dir, "checkout", commit_hash])
    else:
        logs.append(f"Pulling latest commit from branch {branch}")
        response = execute_command(["git", "-C", local_dir, "checkout", branch])
        if response["success"]:
            response = execute_command(["git", "-C", local_dir, "pull", "origin", branch])
    
    return response

def set_permission_readonly(local_dir, exclude_ext, logs):
    for root, _, files in os.walk(local_dir):
        for file in files:
            if not file.endswith(exclude_ext):
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o444)
                logs.append(f"Set {file_path} to read-only.")

def set_permission_full(local_dir, logs):
    for root, _, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, 0o777)
            logs.append(f"Set {file_path} to full permission.")

def create_env_file(local_dir, env_config):
    file_path = os.path.join(local_dir, ".env")
    print(f"Creating .env file at {file_path}")
    with open(file_path, "w") as env_file:
        for key, value in env_config.items():
            env_file.write(f"{key} = '{value}'\n")

if __name__ == "__main__":
    username = get_username()
    server_url = "http://localhost:9000"
    config = load_config()
    local_dir=config.get("local_dir", "./test")
    
    deploy_repo(
        username=username,
        server_url=server_url,
        repo_url=config["repo_url"],
        branch=config.get("branch", "main"),
        commit_hash=config.get("commit_hash"),
        local_dir=config.get("local_dir", "./test"),
        exclude_ext=config.get("exclude_ext", ".ipynb")
    )

    if "env" in config:
        create_env_file(local_dir, config["env"])
