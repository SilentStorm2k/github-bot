from github import Github, GithubIntegration, Auth

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


def isValidAction(eventType, eventStatus):
    if (not eventType in validEvents or not eventStatus in validStatus):
        return 'invalid event: make sure bot has access to ' + eventType
    return eventType