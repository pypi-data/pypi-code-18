from ppg_common.clients.base import BaseClient


class CopperfieldClient(BaseClient):
    urls = {
        "execute": "/v2/operations/execute/{}/{}",
        "status": "/v2/operations/status/{}",
        "abort": "/v2/operations/abort/{}"
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(CopperfieldClient, self).__init__(host, port, ssl, session)

    def show_status(self, file_id):
        return self.get(self.urls.get('status').format(file_id))

    def abort_task(self, file_id):
        return self.get(self.urls.get('abort').format(file_id))

    def execute(self, box, file_id, input_file, command, output_file):
        body = {
            'input_file': input_file,
            'command': command,
            'output_file': output_file
        }
        return self.post(
            self.urls.get('execute').format(box, file_id), body=body
        )
