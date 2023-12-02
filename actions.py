from github import Github
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
    sender = payload['sender']['login']

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
    
    action = headers['X-GitHub-Event']
    status = payload['action']
    valid_bot_commands = {'meme': make_meme, 'help': send_help_docs, 'assign': assign_task}
    comment_event = {'issue_comment' : payload.get("issue", {}).get("number"), 
                     'discussion_comment' : payload.get("discussion", {}).get("number"), 
                     'pull_request_review_comment' : payload.get("pull_request", {}).get("number")}
    # check if event is a supported Github event by this app
    if not is_valid_action(action, status):
        return "invalid request"
    
    if action in comment_event.keys() and (status == "created" or status == "edited"):
        body = payload["comment"]["body"]
        bot_commands = bot_commands_to_execute(input_str=body)
        for commands in bot_commands:
            func = valid_bot_commands[commands]
            if func is not None:
                func_params = inspect.signature(func).parameters
                args = [comment_event[action], git_connection, owner, repo_name, sender, body][:len(func_params)]
                func(*args)
    
    return 'ok'

    

def make_meme(issue_number, git_connection, owner, repo_name):
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

def send_help_docs(issue_number, git_connection, owner, repo_name):
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    issue = repo.get_issue(issue_number)
    f = open('github-bot/data/bot_usage_guide.txt', 'r')
    issue.create_comment(f.read())
    f.close()
    return 'ok'

def assign_task(issue_number, git_connection, owner, repo_name, sender, body):
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    issue = repo.get_issue(issue_number)
    if (not sender == owner):
        return "invalid access"
    assignee = get_assignee(body)
    print(*assignee)
    if not assignee:
        send_help_docs(issue_number, git_connection, owner, repo_name)
    else: 
        try: 
            issue.add_to_assignees(*assignee)
            issue.create_comment(f"Added @{assignee[0]} as an assignee")
        except:
            issue.create_comment("Max number of assignees reached")     
    return 'ok'

def get_assignee(body):
    assignee = []
    words = body.split()
    assign_flag = False

    for word in words:
        if word == '/assign':
            assign_flag = True
        elif assign_flag and word.startswith('@'):
            assignee.append(word[1:])  # Remove '@' symbol
            break  # Break the loop after capturing the first name
        elif assign_flag:
            break
    return assignee

def is_valid_action(eventType, eventStatus):
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

