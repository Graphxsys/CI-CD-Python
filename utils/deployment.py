import os
import subprocess


def execute_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip() if e.stderr else str(e)}

def clone_or_update_repo(repo_url, branch, commit_hash, local_dir, logs):
    if not os.path.exists(local_dir):
        logs.append(f"Cloning repository {repo_url} into {local_dir}...")
        response = execute_command(["git", "clone", "-b", branch, repo_url, local_dir])
    else:
        logs.append("Repository already exists. Fetching latest changes...")
        response = execute_command(["git", "-C", local_dir, "fetch"])
    
    if not response["success"]:
        return response

    if commit_hash:
        logs.append(f"Checking out specific commit {commit_hash}...")
        response = execute_command(["git", "-C", local_dir, "checkout", commit_hash])
    else:
        logs.append(f"Pulling latest commit from branch {branch}...")
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


if __name__ == "__main__":
    print("This script is not meant to be executed directly.")
