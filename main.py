from flask import Flask, request, jsonify

from utils.deployment import execute_command, clone_or_update_repo, set_permission_readonly, set_permission_full
from utils.pyodbc_sql import MSSQLDatabase

app = Flask(__name__)
sql = MSSQLDatabase()

@app.route("/deploy", methods=["POST"])
def deploy():
    data = request.json
    username = data.get("username", "anonymous")
    repo_url = data.get("repo_url")
    branch = data.get("branch", "main")
    commit_hash = data.get("commit_hash")
    local_dir = data.get("local_dir", "./test")
    exclude_ext = data.get("exclude_ext", ".ipynb")
    logs = []
    
    set_permission_full(local_dir, logs)
    response = clone_or_update_repo(repo_url, branch, commit_hash, local_dir, logs)
    if not response["success"]:
        return jsonify({"status": "error", "message": response["error"], "logs": logs}), 500
    
    set_permission_readonly(local_dir, exclude_ext, logs)
    insert_query = f"""INSERT INTO DeploymentLogs (username, repo_url, branch, commit_hash, local_dir, exclude_ext, logs) 
    VALUES 
    {(username, repo_url, branch, commit_hash, local_dir, exclude_ext, "\n".join(logs))}"""
    sql.execute_query(insert_query)

    return jsonify({"status": "success", "message": "Deployment completed.", "logs": logs}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)