import os
import requests

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
    os.path.normpath(os.path.expanduser('~/Code/certificates_keys/roody_ruler_github_bot.pem')), 
    'r'
    # os.path.normpath(os.path.expanduser('/etc/secrets/roody_ruler_github_bot.pem')), 
    # 'r'
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

    execute(headers, payload)

    # check if event is a Github PR creation event
    if not all(k in payload.keys() for k in ['action', 'pull_request']) and \
            payload['action'] == 'opened':
        return "ok"

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    # Get a git connection as our bot
    # Here is where we are getting the permission to talk to our bot
    # and not as a python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_repo_installation(owner, repo_name).id
        ).token
    )

    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(number=payload['number'])

    # prone to change
    # Call meme-api to get a random meme
    response = requests.get(url='https://meme-api.com/gimme/wholesomememes')

    if response.status_code != 200:
        return 'ok'
    
    # Get the best resolution meme??
    meme_url = response.json()['preview'][-1]
    # create comment with random meme
    issue.create_comment(f"![Alt Text]({meme_url})")
    return 'ok'

# For testing locally
if __name__ == '__main__':
    app.run(debug=True, port=5000)