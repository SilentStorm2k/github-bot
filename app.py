import os

from flask import Flask, request
from github import Github, GithubIntegration, Auth
from actions import execute

app = Flask(__name__)

# Github app id of the bot
app_id = '634710'

# private key to authenticate with github
# location for production as dictated by the deployment web service used
# bot certificate
with open(
    # os.path.normpath(os.path.expanduser('~/Code/certificates_keys/roody_ruler_github_bot.pem')), 
    # 'r'
    os.path.normpath(os.path.expanduser('/etc/secrets/roody_ruler_github_bot.pem')), 
    'r'
) as cert_file:
    app_key = cert_file.read()

auth = Auth.AppAuth(app_id, app_key)
# Create github integration instance
git_integration = GithubIntegration(auth=auth)

@app.route("/", methods=['POST'])
def bot():

    # get event headers
    headers = request.headers
    # get event payload
    payload = request.json

    return execute(headers, payload, git_integration)

# For testing locally
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)