import os
from basePhantom import _BasePhantom

class _PhantomPlaybooks(_BasePhantom):
    """
    Wrapper around the Phantom REST calls for Playbooks
    """
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "playbook_run")

    def exists(self, playbook_name):
        url = "%s?_filter_name__contains='%s'" % (os.path.join(self.host, "playbook"),
                                                  playbook_name)
        resp = self.__make_rest_request__(url, "GET")
        return resp["count"] > 0

    def trigger(self, playbook_id, container_id):
        data = dict(
            container_id=container_id,
            playbook_id=playbook_id,
            run=True
        )
        return self.__make_rest_request__(self.endpoint_url, "POST", data=data)

    def get_results(self, playbook_run_id):
        url = os.path.join(self.endpoint_url, playbook_run_id)

        # Start polling the endpoint for the results until the status is not 'running'
        results = None
        while (results is None or results['status'] == 'running'):
            results = self.__make_rest_request__(url, "GET")
            if results is None:
                break

        return results

    def get_full_results(self, playbook_run_id, query=None):
        endpoint_url = os.path.join(self.host, "app_run?_filter_playbook_run_id=%s" % playbook_run_id)
        if query is not None:
            endpoint_url += "&%s" % query
        return self.__make_rest_request__(endpoint_url, "GET")

    def get_app_run_results(self, app_run_id):
        endpoint_url = os.path.join(self.host, "app_run/%s" % app_run_id)
        return self.__make_rest_request__(endpoint_url, "GET")

