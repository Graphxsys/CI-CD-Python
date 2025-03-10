import os
import subprocess

def clone_or_pull_repo(repo_url, branch, local_dir):
    if not os.path.exists(local_dir):
        print(f"Cloning repository {repo_url} into {local_dir}...")
        subprocess.run(["git", "clone", "-b", branch, repo_url, local_dir], check=True)
    else:
        print(f"Repository already exists. Pulling latest changes from {branch}...")
        subprocess.run(["git", "-C", local_dir, "fetch"], check=True)
        subprocess.run(["git", "-C", local_dir, "checkout", branch], check=True)
        subprocess.run(["git", "-C", local_dir, "pull", "origin", branch], check=True)

def make_files_readonly(local_dir, exclude_ext):
    for root, _, files in os.walk(local_dir):
        for file in files:
            if not file.endswith(exclude_ext):
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o444)  # Read-only permission
                print(f"Set {file_path} to read-only.")

if __name__ == "__main__":
    repo_url = "https://github.com/SinkuKumar/CI-CD-Python.git"  # Updated repo URL
    branch = "main"  # Change to the desired branch
    local_dir = "./CI-CD-Python"  # Updated directory name
    exclude_ext = ".py"  # Change this to the extension you want to exclude
    
    try:
        clone_or_pull_repo(repo_url, branch, local_dir)
        print("Repository is up to date.")
        make_files_readonly(local_dir, exclude_ext)
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
