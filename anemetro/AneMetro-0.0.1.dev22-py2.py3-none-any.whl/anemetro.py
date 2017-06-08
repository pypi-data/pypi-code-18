"""
theCodePutter

Puts the code he findses on meetup.
"""

import os
from shutil import copyfile
from subprocess import run
from subprocess import PIPE
from functools import reduce
from pytz import timezone
import pytz
import reyaml
import requests
from anemetro.models import Event
from anemetrohexo import generate_post_filename, process_placeholders, get_template_path

def get_next_event(api_key, api_root, group_name):
    """Returns the next meetup event."""
    url = "{0}/{1}/events".format(api_root, group_name)
    params = {
        "scroll": "next_upcoming",
        "page": "1",
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()[0]

    data["time"] = data["time"] / 1000 # MeetUp gives timestamp in milliseconds
    data["updated"] = data["updated"] / 1000 # MeetUp gives timestamp in milliseconds

    event = Event(venue_name=data["venue"]["name"], **data)
    return event

def get_git_url(config_filename, path_to_git_setting):
    """Reads the git url from the given yaml config file"""
    config = reyaml.load_from_file(config_filename)
    return reduce((lambda cur, item: cur[item]), path_to_git_setting.split("/"), config)

def commit_post(filename, git_url, message="Auto commit by thePutter", branch_name="master"):
    """Stages, commits, and pushes the created post"""
    if did_post_change(filename):
        print("Post changed: %s, pushing it." % filename)
        run(["git", "remote", "rm", "putter"])
        run(["git", "remote", "add", "putter", git_url])
        run(["git", "add", filename])
        run(["git", "commit", "-m", message])

        # The build runs in detached head state. This works, but, I'm not sure
        # what sideeffects this may have. Something I'll look into.
        run(["git", "push", "putter", "HEAD:" + branch_name])
    else:
        print("Post did NOT change: %s" % filename)

def did_post_change(filename):
    """Checks if the post filename changed or was created due to the generation process"""
    status = run(["git", "status", "-s"], stdout=PIPE, universal_newlines=True).stdout
    lines = status.split("\n")
    if " M %s" % filename in lines or "?? %s" % filename in lines:
        return True
    else:
        return False

def generate_post(template, destination_folder, event):
    """Generates event post file"""

    # Create initial post from template
    file_name = generate_post_filename(event)
    full_filename = destination_folder + "/" + file_name
    copyfile(template, full_filename)

    content = process_placeholders(full_filename, event)

    # Saving processed content
    with open(full_filename, mode="w") as post_file:
        for line in content:
            post_file.write(line)

    return full_filename

def get_putter_config(filename="anemetro.yml"):
    """Gets the config to use for processing"""
    return reyaml.load_from_file(filename)

def putt():
    """Runs the processing"""
    config = get_putter_config()
    event = get_next_event(config["meetup_apikey"], config["meetup_root"], config["group_name"])
    event.set_timezone(timezone(config["group_timezone"]))
    template_path = get_template_path(config["template_name"])
    post_filename = generate_post(template_path, config["posts_path"], event)

    git_url = get_git_url(config["yaml_filename"], config["yaml_query"])
    commit_post(post_filename, git_url, branch_name=config["posts_branch"])
