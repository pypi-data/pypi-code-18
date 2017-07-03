import json
import time

import urllib3

from dashbase.utils import rpc
from dashbase.utils.errors import CliRuntimeError


class AdminHealthChecker:
    def __init__(self, num_tries=5, delay_in_sec=5):
        self.num_tries = num_tries
        self.delay_in_sec = delay_in_sec

    def do_healthcheck(self):
        return True

    def check_health(self):
        healthy = False
        for _ in range(self.num_tries):
            try:
                healthy = self.do_healthcheck()
                if healthy:
                    break
                else:
                    time.sleep(self.delay_in_sec)
            except ValueError as err:
                print("Problem executing query, will try again: " + str(err))
        return healthy

    def close(self):
        pass


class DropWizardAdminHealthChecker(AdminHealthChecker):
    def __init__(self, host_port, num_tries=5, delay_in_sec=5):
        AdminHealthChecker.__init__(self, num_tries, delay_in_sec)
        self.rpc = rpc.RPC(host_port)

    @staticmethod
    def parse_health_response(health_resp):
        healthy = False
        for key, value in list(health_resp.items()):
            if "healthy" in value:
                healthy = value["healthy"]
                if not healthy:
                    print("Health check failed for {}".format(key))
                    break
            else:
                raise CliRuntimeError("Health check endpoint does not exist.")
        return healthy

    def do_healthcheck(self):
        print("Initiating health check...")
        try:
            resp = self.rpc.do_get("/admin/healthcheck")
            data = resp.data
            health_resp = json.loads(data)
            return DropWizardAdminHealthChecker.parse_health_response(health_resp)
        except urllib3.exceptions.MaxRetryError:
            self.rpc.close()
            self.rpc.init_connection()
            raise CliRuntimeError("connection to health check failed. "
                                  "Either the service did not start due to "
                                  "configuration problems or connection to "
                                  "ZooKeeper failed.")
        except urllib3.exceptions.HTTPError:
            self.rpc.close()
            self.rpc.init_connection()
            raise

    def close(self):
        print("Closing health check connection...")
        self.rpc.close()
