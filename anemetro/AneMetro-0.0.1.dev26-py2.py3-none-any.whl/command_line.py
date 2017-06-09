from anemetro.anemetro import putt
import os.path
import textwrap
import sys

def main():
    test = "test" in sys.argv
    putt(test) # FORE!

def config():
    full_path = os.path.abspath("./anemetro.yml")
    if os.path.exists(full_path):
        print("The %s config file already exists." % full_path)
    else:
        default = textwrap.dedent("""\
        # AneMetro Config
        meetup_root: "https://api.meetup.com"
        group_name: "PUT_MEETUP_URL_GROUP_NAME_HERE"
        group_timezone: "US/Central"
        template_name: "meetup"
        posts_path: "source/_posts"

        # **DO NOT** put your real MeetUp API key in here into source control.
        # Do that via your build environment variables.
        # You have been warned.
        meetup_apikey: "PUT_KEY_HERE"

        # Config for committing new post to the repo and pushing.
        #
        posts_branch: "master"

        # Where to get the git url to push to.
        yaml_filename: "_config.yml"
        yaml_query: "deploy/repository"
        """)
        with open(full_path, mode="w") as config_file:
            config_file.write(default)

def config_codefresh():
    if len(sys.argv) != 2:
        print("You must specify the name of the repository as the one and only argument.")
        return

    repository = sys.argv[1]
    full_path = os.path.abspath("./codefresh.yml")
    if os.path.exists(full_path):
        print("The %s config file already exists." % full_path)
    else:
        default = textwrap.dedent("""\
        version: "1.0"
        steps:
            get_latest_meetup:
                image: python:latest
                commands:
                    - git config --global user.name "AneMetro"
                    - git config --global user.email "anemetro@example.com"
                    - sed -i'' "s~https://github.com/techlahoma/{{REPOSITORY}}.git~https://${GH_TOKEN}:x-oauth-basic@github.com/techlahoma/{{REPOSITORY}}.git~" _config.yml
                    - sed -i'' "s~PUT_KEY_HERE~${MEETUP_TOKEN}~" anemetro.yml
                    - pip install anemetro
                    - anemetro-pull
                when:
                    condition:
                        all:
                            explicitlyRun: "'${{CF_BUILD_TRIGGER}}' == 'build'"
            deploy_site:
                image: node:4
                commands:
                    - rm -rf node_modules/
                    - npm install
                    - npm install -g hexo-cli --no-optional
                    - git config --global user.name "AneMetro"
                    - git config --global user.email "anemetro@example.com"
                    - sed -i'' "s~https://github.com/techlahoma/{{REPOSITORY}}.git~https://${GH_TOKEN}:x-oauth-basic@github.com/techlahoma/{{REPOSITORY}}.git~" _config.yml
                    - rm -rf .deploy_git/
                    - hexo clean
                    - hexo generate
                    - hexo deploy
                when:
                    branch:
                        only:
                            - master
        """).replace("{{REPOSITORY}}", repository)
        with open(full_path, mode="w") as config_file:
            config_file.write(default)
        print("CodeFresh config added.")
        print("Make sure you create the appropriate enivronment variables in your CodeFresh build account.")
        print("  MEETUP_TOKEN which needs to have your API key for MeetUp.com.")
        print("  GH_TOKEN which needs your Github personal access token.")
