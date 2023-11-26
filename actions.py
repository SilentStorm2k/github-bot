from github import Github, GithubIntegration, Auth
import requests

validEvents = ['issues', 'issue_comment', 'member', 'installation', 'check_suite', 'discussion', \
                'discussion_comment', 'pull_request_review', 'pull_request_review_thread', \
                'pull_request', 'pull_request_review_comment', 'status']
validStatus = ['assigned', 'closed', 'deleted', 'demilestoned', 'edited', 'labeled', 'locked', 'milestoned', \
               'opened', 'pinned', 'reopened', 'transferred', 'unassigned', 'unlabeled', 'unlocked', 'unpinned', \
               'added', 'dismissed', 'submitted', 'resolved', 'unresolved', 'answered', 'category_changed', \
               'created', 'auto_merge_disabled', 'auto_merge_enabled', 'converted_to_draft', 'dequeued', \
               'enqueued', 'ready_for_review', 'review_request_removed', 'review_requested', \
               'synchronize', 'error', 'failure', 'pending', 'success']

def execute(headers, payload, git_integration):

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']
    sender = payload.get("sender", {}).get("login")

    if (sender == "roody-ruler[bot]"):
        return "Bot message, ignore"
    
    # Get a git connection as our bot
    # Here is where we are getting the permission to talk to our bot
    # and not as a python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_repo_installation(owner, repo_name).id
        ).token
    )
    
    action = headers.get('X-GitHub-Event')
    status = payload.get('action')
    # check if event is a supported Github event by this app
    if not isValidAction(action, status):
        return "invalid request"
    
    if action == "issue_comment" and (status == "created" or status == "edited"):
        if "/meme" in payload.get("comment", {}).get("body"):
            return makeMeme(issue_number=payload.get("issue", {}).get("number"), git_connection=git_connection, owner=owner, repo_name=repo_name)
    
    return 'ok'

    

def makeMeme(issue_number, git_connection, owner, repo_name):
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(issue_number)

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


def isValidAction(eventType, eventStatus):
    if (not eventType in validEvents or not eventStatus in validStatus):
        # For debugging:
        # print("invalid event: make sure bot has access to " + eventType)
        return False
    return True