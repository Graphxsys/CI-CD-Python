"""
SMTP Email
----------

This module contains classes to send emails using SMTP server. It also contains email templates for sending emails.

:module: smtp_email.py
:platform: Unix, Windows
:synopsis: Send emails using SMTP server and email templates.

:date: March 3, 2025
:author: Sinku Kumar `sinkukumar.r@hq.graphxsys.com <mailto:sinkukumar.r@hq.graphxsys.com>`
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class EmailSender:
    def __init__(
        self,
        smtp_server,
        smtp_port,
        sender_email,
        sender_password,
        cc_emails=None,
        bcc_emails=None,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.cc_emails = cc_emails
        self.bcc_emails = bcc_emails

    def send_email(
        self,
        receiver_emails,
        subject,
        html_body,
        image_path=None,
    ):
        try:
            # Create message container
            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(receiver_emails)
            msg["Subject"] = subject

            # Add CC and BCC if provided
            if self.cc_emails:
                msg["Cc"] = ", ".join(self.cc_emails)
            if self.bcc_emails:
                msg["Bcc"] = ", ".join(self.bcc_emails)

            # Attach HTML body
            msg.attach(MIMEText(html_body, "html"))

            # Attach image if provided
            if image_path:
                with open(image_path, "rb") as img_file:
                    img = MIMEImage(img_file.read())
                    img.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=os.path.basename(image_path),
                    )
                    msg.attach(img)

            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                text = msg.as_string()
                all_recipients = (
                    receiver_emails
                    + (self.cc_emails if self.cc_emails else [])
                    + (self.bcc_emails if self.bcc_emails else [])
                )
                server.sendmail(self.sender_email, all_recipients, text)
                logging.info(f"Email sent successfully to: {receiver_emails}")
        except Exception as send_email_exception:
            raise Exception(f"Unable to send email: {send_email_exception}.")


class EmailTemplate:
    # TODO: Implement templates for your email notifications here
    def deployment_notification(self, username, repo_url, branch, commit_hash, local_dir, exclude_ext, status, message, created_at, logs):
        """
        HTML template for deployment notification email
        """
        return (
            f'{username} has deployed the python script.',
            f"""
            <!DOCTYPE html>
            <html>
              <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Deployment Notification</title>
                <style>
                  body {{
                    font-family: Arial, sans-serif;
                    background-color: #eef2f7;
                    padding: 10px;
                  }}
                  .container {{
                    background: #ffffff;
                    padding: 10px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    margin: auto;
                  }}
                  .header {{
                    font-size: 22px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 15px;
                    text-align: center;
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 10px;
                  }}
                  .details {{
                    margin-bottom: 15px;
                    line-height: 1.6;
                    color: #555;
                  }}
                  .details strong {{
                    color: #333;
                  }}
                  .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                    margin-top: 15px;
                  }}
                  .logs {{
                    background-color: #1E1E1E;
                    color: #F2F2F2;
                    font-family: 'Courier New', Courier, monospace; /* Monospace font */
                    padding: 10px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    overflow-wrap: break-word;  /* Ensures text wraps correctly */
                    overflow-y: auto;
                    max-height: 400px;
                    border: 1px solid #333;
                  }}
                  
                  .logs p {{
                    margin: 0;
                    line-height: 1.2; /* Compact but readable */
                    white-space: pre-wrap;
                  }}
                  
                  .logs br {{
                    display: inline;
                  }}
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="header">Deployment Notification</div>
                  <div class="details">
                    <strong>Username:</strong> {username}<br />
                    <strong>Repository URL:</strong>
                    <a href="{repo_url}" style="color: #007bff; text-decoration: none">{repo_url}</a><br />
                    <strong>Branch:</strong> {branch}<br />
                    <strong>Commit Hash:</strong> {commit_hash}<br />
                    <strong>Local Directory:</strong> {local_dir}<br />
                    <strong>Excluded Extensions:</strong> {exclude_ext}<br />
                    <strong>Status:</strong>
                    <span style="font-weight: bold; color: {"green" if status == "success" else "red"};">
                      {status}
                    </span><br />
                    <strong>Message:</strong> {message}<br />
                    <strong>Created At:</strong> {created_at}
                  </div>
                  <div class="logs">
                    <p>{logs.replace('\n', '<br>')}<p>
                  </div>
                  <br><br>
                  <hr>
                  <div class="footer">
                    This is an automated notification. Please do not reply.
                  </div>
                </div>
              </body>
            </html>
            """,
            )


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    
    smtp_server = os.getenv("SMTP_ADDRESS")
    smtp_port = os.getenv("SMTP_PORT")
    sender_email = os.getenv("SMTP_ACCOUNT")
    sender_password = os.getenv("SMTP_PASSWORD")

    receiver_email = ["sinkukumar.r@hq.graphxsys.com"]

    email_template = EmailTemplate()
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    subject, html_body = email_template.deployment_notification('Sinku', 'https://github.com/SinkuKumar/CI-CD-Python.git', 'main',
                                                                '72a3eb3f83fc6f148d343f869070f067c44b4d4e', './Users/Sinku/Desktop/Deployment',
                                                                '.ipynb', 'success', 'Deployment completed', '2025-03-11 05:07:15.847',
                                                                'Cloning repository https://github.com/SinkuKumar/CI-CD-Python.git into ./Users/Sinku/Desktop/Deployment...\nChecking out specific commit 72a3eb3f83fc6f148d343f869070f067c44b4d4e...\nSet ./Users/Sinku/Desktop/Deployment/pull_repo.py to read-only.\nSet ./Users/Sinku/Desktop/Deployment/another_test.txt to read-only.\nSet ./Users/Sinku/Desktop/Deployment/README.md to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.gitignore to read-only.\nSet ./Users/Sinku/Desktop/Deployment/test.txt to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/config to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/HEAD to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/description to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/index to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/packed-refs to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/objects/pack/pack-f73fd1f94018164a61be19992aa83b39a64bee4a.idx to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/objects/pack/pack-f73fd1f94018164a61be19992aa83b39a64bee4a.pack to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/info/exclude to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/logs/HEAD to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/logs/refs/heads/main to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/logs/refs/remotes/origin/HEAD to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/commit-msg.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/pre-rebase.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/pre-commit.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/applypatch-msg.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/fsmonitor-watchman.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/pre-receive.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/prepare-commit-msg.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/post-update.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/pre-merge-commit.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/pre-applypatch.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/pre-push.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/update.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/hooks/push-to-checkout.sample to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/refs/heads/main to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.git/refs/remotes/origin/HEAD to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.vscode/settings.json to read-only.\nSet ./Users/Sinku/Desktop/Deployment/.vscode/extensions.json to read-only.')
    email_sender.send_email(receiver_email, subject, html_body)
    logging.info("Sent SMS email.")