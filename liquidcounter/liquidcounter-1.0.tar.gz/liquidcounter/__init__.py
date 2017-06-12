import copy
STANDARD_VOTES = ['yes', 'no', 'abstain']


def notResolved(liquid={}):
    votes = []
    for vote in liquid:
        votes += liquid[vote]
    return set(liquid.keys()).intersection(votes)


def _flattenList(l=[]):
    return [item for sublist in l for item in sublist]


def _resolveLiquids(liquid={}):
    old_liquid = copy.deepcopy(liquid)
    keepWorking = True
    while keepWorking:
        mustChange = False
        for vote in liquid:
            for voter in liquid[vote]:
                if voter in liquid:
                    liquid[vote] += liquid[voter]
                    mustChange = True
                    break
            if mustChange:
                break
        if mustChange:
            del liquid[voter]
        keepWorking = len(notResolved(liquid)) != 0

    abstain = len(_flattenList(old_liquid.values())) - len(_flattenList(liquid.values()))
    if abstain != 0:
        liquid['abstain'] = abstain
    return liquid


def resolveIt(votes={}):
    results = {
        'yes': 0,
        'no': 0,
        'abstain': 0,
        'liquid': 0
    }

    liquid = {}
    voters = []

    if votes != {}:
        for vote in votes:
            if vote not in STANDARD_VOTES:
                for voter in votes[vote]:
                    if voter not in voters:
                        voters.append(voter)
                    else:
                        RuntimeError('There are two or more votes from: ' + voter)
                if vote in liquid:
                    liquid[vote] += votes[vote]
                else:
                    liquid[vote] = votes[vote]

        for vote in liquid:
            del votes[vote]

        liquid = _resolveLiquids(liquid)

        if 'abstain' in liquid:
            results['abstain'] = liquid['abstain']
            del liquid['abstain']

        for vote in STANDARD_VOTES:
            if vote in votes:
                for voter in votes[vote]:
                    if voter not in voters:
                        voters.append(voter)
                    else:
                        raise RuntimeError('There are two or more votes from: ' + voter)
                    if voter in liquid:
                        results[vote] += len(liquid.pop(voter)) + 1
                    else:
                        results[vote] += 1
                del votes[vote]

        for unresolved in liquid:
            results['liquid'] += len(liquid[unresolved])

        if len(votes) != 0:
            raise RuntimeError('There are votes that have not being counted for some reason. Check implementation')
    return results
