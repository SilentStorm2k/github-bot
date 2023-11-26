from github import Github, GithubIntegration, Auth
import requests
import inspect

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
    valid_bot_commands = {'meme': makeMeme}
    comment_event = {'issue_comment' : payload.get("issue", {}).get("number"), 
                     'discussion_comment' : payload.get("discussion", {}).get("number"), 
                     'pull_request_review_comment' : payload.get("pull_request", {}).get("number")}
    # check if event is a supported Github event by this app
    if not isValidAction(action, status):
        return "invalid request"
    
    if action in comment_event.keys() and (status == "created" or status == "edited"):
        bot_commands = bot_commands_to_execute(input_str=payload.get("comment", {}).get("body"))
        for commands in bot_commands:
            func = valid_bot_commands.get(commands)
            if func is not None:
                func_params = inspect.signature(func).parameters
                args = [comment_event.get(action), git_connection, owner, repo_name][:len(func_params)]
                func(*args)
    
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

def bot_commands_to_execute(input_str):
    commands = input_str.split()
    commands_set = set()

    for i, word in enumerate(commands):
        if word.startswith("/"):
            commands_set.add(word[1:])  # Adding the word after the '/'
    
    return commands_set

