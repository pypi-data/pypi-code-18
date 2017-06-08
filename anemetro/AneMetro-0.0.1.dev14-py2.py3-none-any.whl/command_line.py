from anemetro.anemetro import putt
import os.path
import textwrap

def main():
    putt() # FORE!

def config():
    full_path = os.path.abspath("./anemetro.yml")
    if os.path.exists(full_path):
        print("The %s config file already exists." % full_path)
    else:
        default = textwrap.dedent("""# AneMetro Config
        meetup_root: "https://api.meetup.com"
        meetup_apikey: "PUT_KEY_HERE"
        group_name: "PUT_MEETUP_URL_GROUP_NAME_HERE"
        group_timezone: "US/Central"
        template_name: "meetup"
        posts_path: "source/_posts"

        # Config for committing new post to the repo and pushing.
        #
        posts_branch: "master"

        # Where to get the git url to push to.
        yaml_filename: "_config.yml"
        yaml_query: "deploy/repository"
        """)
        with open("anemetro.yml", mode="w") as config_file:
            config_file.write(default)
