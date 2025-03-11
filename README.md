# CI/CD Pipeline for Python

This repository provides a custom CI/CD pipeline for deploying Python scripts efficiently.

## Project Setup

### 1. Use Git Template

Always use the Git template repository to create your project. It contains the necessary template code required for developing automation scripts. You can access it here: [PyBase GitHub Repository](https://github.com/Graphxsys/PyBase).

### 2. Set Up a Virtual Environment

To develop your script, always create a new virtual environment using Python **3.10.11**, as this is the version used in the production server.

#### Steps to Set Up the Virtual Environment:

```sh
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

### 3. Install and Manage Dependencies

During development, use `pip` to install additional packages. Before pushing changes to GitHub, update the `requirements.txt` file:

```sh
pip freeze > requirements.txt
```

This ensures that all required dependencies are stored and can be installed in production.

## Deployment Setup

### 1. Prepare `deployment.yaml`

Before deploying the script, ensure your `deployment.yaml` file is available at the root of the project. This file specifies the necessary environment variables and deployment settings.

Example `deployment.yaml` format:

```yaml
repo_url: "https://github.com/SinkuKumar/CI-CD-Python.git"
branch: "main"
commit_hash: "72a3eb3f83fc6f148d343f869070f067c44b4d4e"
local_dir: "./Users/Sinku/Desktop/Deployment"
exclude_ext: ".ipynb"

env:
  # SMTP Server Credentials
  SMTP_ADDRESS: "smtp.abc.com"
  SMTP_PORT: 587
  SMTP_ACCOUNT: "email@graphxsys.com"
  SMTP_PASSWORD: "password"

  # SQL Server Credentials
  SQL_SERVER: "127.0.0.1"
  SQL_DATABASE: "CI_CD"
  SQL_USERNAME: "sa"
  SQL_PASSWORD: "Password@123"
```

### 2. Push Changes to GitHub

To commit and push your changes, use the following commands:

```sh
git add .
git commit -m "Your commit message"
git pull
git push
```

### 3. Trigger Deployment

Once the code is pushed to GitHub, trigger the deployment script by running:

```sh
python utils/deployment.py
```

## Rollback to a Previous Commit

If you encounter an issue after deployment, you can revert to a previous commit using `git log`, which provides commit history.

Example:

```sh
(venv) Sinku@Macbook4 CI-CD-Python % git log
commit f96b8b261cf08040c023e2328366dfb751404629 (HEAD -> main, origin/main, origin/HEAD)
Author: SinkuKumar <sudosinku@gmail.com>
Date:   Tue Mar 11 14:32:25 2025 +0530

    Add deployment configuration and enhance deployment functionality
```

To deploy a specific commit, update the `commit_hash` in `deployment.yaml` and redeploy the script. This ensures that your project rolls back to the desired checkpoint.

## Note

**Use commit hash only if you want to rollback to a specific checkpoint, else leave it empty.**

## Conclusion

This CI/CD pipeline helps streamline Python script deployment while maintaining consistency across environments. Follow the best practices outlined in this document to ensure smooth development and deployment processes.

## Disclaimer

This document may contain errors or omissions. If you find any, please report them to **sinkukumar.r@hq.graphxsys.com** or **bi@graphxsys.com**.

This approach has been designed based on the team's understanding and requirements. There may be other, potentially better, ways to achieve the same outcome. However, this implementation is based on my best efforts, understanding, and learning at Graphxsys.
