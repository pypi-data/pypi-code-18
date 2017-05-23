import tamme

def testpypi():
    return "This is packaged correctly"


def track(write_key, identity_id, event_name, traits):
    return tamme.track(write_key, identity_id, event_name, traits)


def identify(write_key, identity_id, traits):
    return tamme.identify(write_key, identity_id, traits)


def alias(write_key, old_id, new_id):
    return tamme.alias(write_key, old_id, new_id)


def flush():
    return None
