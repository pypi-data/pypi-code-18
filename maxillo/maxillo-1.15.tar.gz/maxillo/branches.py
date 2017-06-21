import maxillo.applications

def get(uuid, branch):
    return {
        'application'   : maxillo.applications.get(uuid),
        'name'          : branch,
    }
