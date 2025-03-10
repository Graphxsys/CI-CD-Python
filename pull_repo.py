import os
import subprocess

def clone_or_update_repo(repo_url, branch, commit_hash, local_dir):
    if not os.path.exists(local_dir):
        print(f"Cloning repository {repo_url} into {local_dir}...")
        subprocess.run(["git", "clone", "-b", branch, repo_url, local_dir], check=True)
    else:
        print(f"Repository already exists. Fetching latest changes...")
        subprocess.run(["git", "-C", local_dir, "fetch"], check=True)

    if commit_hash:
        print(f"Checking out specific commit {commit_hash}...")
        subprocess.run(["git", "-C", local_dir, "checkout", commit_hash], check=True)
    else:
        print(f"Pulling latest commit from branch {branch}...")
        subprocess.run(["git", "-C", local_dir, "checkout", branch], check=True)
        subprocess.run(["git", "-C", local_dir, "pull", "origin", branch], check=True)

def set_permission_readonly(local_dir, exclude_ext):
    for root, _, files in os.walk(local_dir):
        for file in files:
            if not file.endswith(exclude_ext):
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o444)  # Read-only permission
                print(f"Set {file_path} to read-only.")

def set_permission_full(local_dir):
    for root, _, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, 0o777)  # Full permission
            print(f"Set {file_path} to full permission.")

if __name__ == "__main__":
    repo_url = "https://github.com/SinkuKumar/CI-CD-Python.git"  # Repository URL
    branch = "main"  # Default branch
    commit_hash = '72a3eb3f83fc6f148d343f869070f067c44b4d4e'  # Set to a specific commit hash or leave as None
    local_dir = "./test"  # Local directory to store the repo
    exclude_ext = ".py"  # Exclude .py files from read-only permissions
    
    try:
        set_permission_full(local_dir)
        clone_or_update_repo(repo_url, branch, commit_hash, local_dir)
        print(f"Repository is now at {'commit ' + commit_hash if commit_hash else 'latest branch state'}")
        set_permission_readonly(local_dir, exclude_ext)
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
