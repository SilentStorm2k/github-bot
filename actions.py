validEvents = ['issues', 'issue_comment', 'member', 'installation', 'check_suite', 'discussion', \
                'discussion_comment', 'pull_request_review', 'pull_request_review_thread', \
                'pull_request', 'pull_request_review_comment', 'status']
validStatus = ['assigned', 'closed', 'deleted', 'demilestoned', 'edited', 'labeled', 'locked', 'milestoned', \
               'opened', 'pinned', 'reopened', 'transferred', 'unassigned', 'unlabeled', 'unlocked', 'unpinned', \
               'added', 'dismissed', 'submitted', 'resolved', 'unresolved', 'answered', 'category_changed', \
               'created', 'auto_merge_disabled', 'auto_merge_enabled', 'converted_to_draft', 'dequeued', \
               'enqueued', 'ready_for_review', 'review_request_removed', 'review_requested', \
               'synchronize', 'error', 'failure', 'pending', 'success']

def execute(headers, payload):

    pass #place holder for now


def isValidAction(eventType, eventStatus) {
    if (not eventType in validEvents or not eventStatus in validStatus)
        return 'invalid event: make sure bot has access to ' + eventType
    return eventType
}