import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from utils.pyodbc_sql import MSSQLDatabase
from utils.smtp_email import EmailSender, EmailTemplate
from utils.deployment import clone_or_update_repo, set_permission_readonly, set_permission_full

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_ADDRESS")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_ACCOUNT = os.getenv("SMTP_ACCOUNT")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

app = Flask(__name__)
sql = MSSQLDatabase()
email_sender = EmailSender(SMTP_SERVER, SMTP_PORT, SMTP_ACCOUNT, SMTP_PASSWORD)
email_template = EmailTemplate()

email_receivers = ["sinkukumar.r@hq.graphxsys.com"]

@app.route("/deploy", methods=["POST"])
def deploy():
    try:
        data = request.json
        username = data.get("username", "anonymous")
        repo_url = data.get("repo_url")
        branch = data.get("branch", "main")
        commit_hash = data.get("commit_hash")
        local_dir = data.get("local_dir", "./test")
        exclude_ext = data.get("exclude_ext", ".ipynb")
        env_config = data.get("env", {})
        logs = []
        
        set_permission_full(local_dir, logs)
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        response = clone_or_update_repo(repo_url, branch, commit_hash, local_dir, logs)
        str_logs = "\n".join(logs)
        html_logs = "<br>".join(logs)
        if not response["success"]:
            failure_query = f"""INSERT INTO DeploymentLogs (username, repo_url, branch, commit_hash, local_dir, exclude_ext, status, message, logs) 
                            VALUES 
                            {(username, repo_url, branch, commit_hash, local_dir, exclude_ext, 'error', )}"""
            sql.execute_query(failure_query)
            subject = f"Deployment failed for {repo_url}"
            body = email_template.deployment_notification(username, repo_url, branch, commit_hash, local_dir, exclude_ext, "error", response["error"], time_stamp, html_logs)[1]
            email_sender.send_email(email_receivers, subject, body)
            return jsonify({"status": "error", "message": response["error"], "logs": logs}), 500
        
        set_permission_readonly(local_dir, exclude_ext, logs)
        insert_query = f"""INSERT INTO DeploymentLogs (username, repo_url, branch, commit_hash, local_dir, exclude_ext, status, message, logs) 
        VALUES 
        {(username, repo_url, branch, commit_hash, local_dir, exclude_ext, 'success', 'Deployment completed', str_logs)}"""
        sql.execute_query(insert_query)
        subject, body = email_template.deployment_notification(username, repo_url, branch, commit_hash, local_dir, exclude_ext, "success", "Deployment completed", time_stamp, html_logs)
        email_sender.send_email(email_receivers, subject, body)
        return jsonify({"status": "success", "message": "Deployment completed.", "logs": logs}), 200
    
    except Exception as e:
        error_message = str(e)
        return jsonify({"status": "error", "message": error_message}), 500

if __name__ == "__main__":
    try:
        app.run(port=9000, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
