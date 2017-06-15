import requests
from html.parser import HTMLParser
from pyyamlconfig import (
    load_config,
    PyYAMLConfigError,
)
from os.path import expanduser


class BuildsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (key, value) in attrs:
                if key == 'href':
                    if value.startswith('/job/'):
                        parts = value.split('/')
                        if len(parts) == 4:
                            self.result.append(parts[2])


class JenkinsControl:
    def __init__(self, url):
        try:
            self.config = load_config(expanduser('~/.config/jenkins_control.yaml'))
            self.config_loaded = True
        except PyYAMLConfigError:
            self.config_loaded = False
        if url is None:
            if self.config_loaded is True:
                self.url = self.config.get('url')
            else:
                raise Exception('No url provided on commandline or in config file')
        else:
            self.url = url
        self.session = requests.session()

    def get_jobs(self, computer):
        response = requests.get(
            '{}/computer/{}/ajaxExecutors'.format(
                self.url,
                computer,
            ),
        )
        if response.status_code == 200:
            buildsparser = BuildsParser()
            buildsparser.feed(response.text)
            return buildsparser.result
        else:
            raise Exception('Could not find jobs for node')

    def job_running_on_computer(self, job, computer):
        return job in self.get_jobs(computer)

    def get_status(self, computer):
        response = requests.get(
            '{}/computer/{}/api/json'.format(
                self.url,
                computer,
            )
        )
        if response.status_code == 200:
            computer_status = response.json()
            if computer_status.get('offline') is True:
                offline_cause = computer_status.get('offlineCauseReason')
                if offline_cause != '':
                    return "offline ({})".format(offline_cause)
                else:
                    return "offline"
            elif computer_status.get('idle') is True:
                return "idle"
            else:
                return "building"
        else:
            raise Exception('Could not find status for node')

    def status(self, computer):
        computer_status = self.get_status(computer)
        jobs = self.get_jobs(computer)
        if len(jobs) == 0:
            jobs_string = 'No active jobs'
        else:
            jobs_string = 'Active jobs: {}'.format(', '.join(jobs))
        print(
            '{} is {}. {}'.format(
                computer,
                computer_status,
                jobs_string,
            )
        )

    def toggle_offline(self, computer, reason):
        response = self.session.post(
            '{}/computer/{}/toggleOffline'.format(
                self.url,
                computer,
            ),
            data={"offlineMessage": reason},
            auth=(
                self.config.get('username'),
                self.config.get('apitoken'),
            ),
        )
        if response.status_code == 200:
            return True
        else:
            raise Exception(
                '{}: {}'.format(
                    response.status_code,
                    response.text,
                )
            )

    def get_computers_in_label(self, label):
        response = requests.get(
            '{}/label/{}/api/json'.format(
                self.url,
                label,
            )
        )
        if response.status_code == 200:
            info = response.json()
            nodes = info.get('nodes', {})
            return sorted([x.get('nodeName') for x in nodes])
        else:
            raise Exception('Could not fetch label')
