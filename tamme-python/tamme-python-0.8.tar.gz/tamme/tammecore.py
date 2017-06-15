import requests
import os
import sys
import time
LIBRARY = "tamme-python"
VERSION = "0.8"
TAMME_BATCH = []
BASE_PARAMS = {
    "version": VERSION,
    "library": LIBRARY
}
BATCH_SIZE = 5

def track(write_key, identity_id, event_name, traits):
    event_params = BASE_PARAMS.copy()
    event_params["write_key"] = write_key
    event_params["identity_id"] = identity_id
    event_params["name"] = event_name

    event_params["traits"] = normalizeTraits(traits)

    event_params["event_type"] = "track"
    return attachEvent(event_params)


def identify(write_key, identity_id, traits):
    event_params = BASE_PARAMS.copy()
    event_params["write_key"] = write_key
    event_params["event_type"] = "identify"
    event_params["identity_id"] = identity_id
    event_params["traits"] = traits
    return attachEvent(event_params)


def alias(write_key, old_id, new_id):
    event_params = BASE_PARAMS.copy()
    event_params["write_key"] = write_key
    event_params["event_type"] = "alias"
    event_params["new_id"] = new_id
    event_params["previous_id"] = old_id
    return attachEvent(event_params)


def flush():
    global TAMME_BATCH
    params = {
        "account_id": "honeypotisthisrealornotyoutellme",
        "events": list(TAMME_BATCH)
    }
    TAMME_BATCH = []
    return postToTamme(params)


def attachEvent(event_params):
    global TAMME_BATCH
    TAMME_BATCH.append(event_params)
    if len(TAMME_BATCH) >= BATCH_SIZE:
        flush()
    return None


def normalizeTraits(traits):
    if traits is None:
        traits = {}
    if "timestamp" not in traits:
        traits["timestamp"] = time.time() * 1000
    if "version" not in traits:
        traits["version"] = VERSION
    if "library" not in traits:
        traits["library"] = LIBRARY
    return traits


def postToTamme(payload):
    environment = os.environ.get("TAMME_ENV", "production")
    endpoint = "https://" + environment + "-analytics.tamme.io/stream"
    return requests.post(endpoint, json=payload)
