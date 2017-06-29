import logging
import os.path
import untangle
from xml.sax._exceptions import SAXParseException
from datetime import datetime, date, timedelta
from requests import get
from requests.exceptions import ConnectionError

log = logging.getLogger('becbacnet')

logging.basicConfig(level=logging.WARNING)

headers = {
    # "Accept": "application/json"
}
fmt = "%Y-%m-%d"

class EntelliwebError(Exception):
    pass

class EntelliwebUnavailable(EntelliwebError):
    pass

class EnteliwebClient(object):
    """A client for becbacnet Energy Suite API"""

    def __init__(self, base_uri, org):
        self.base_uri = base_uri
        self.org = org

    def uri(self, endpoint):
        return "{}/enteliweb/{}/{}".format(self.base_uri, self.org, endpoint)

    def get(self, *args, **kwargs):
        uri = self.uri(args[0])
        log.debug("connecting to {}".format(uri))
        try:
            return get(uri, *args[1:], **kwargs)
        except ConnectionError as exc:
            raise EntelliwebUnavailable(exc)

    def resource(self):
        response = self.get('resource', headers=headers)
        return [r.cdata for r in untangle.parse(response.text).ResourceList.Resource]

    def consumption(self, meter_list, start_time, end_time, interval, resource):
        payload = {
            "meterlist[]": meter_list,
            "start": start_time.strftime(fmt),
            "end": end_time.strftime(fmt),
            "interval": interval,
            "resource": resource,
            "search": "id"
        }
        response = self.get('data', params=payload, headers=headers)
        if response.status_code != 200:
            raise EntelliwebError("HTTP {}: {}".format(response.status_code, response.text))
        data = untangle.parse(response.text)
        try:
            data = data.ReportData
        except AttributeError as exc:
            if data.Error:
                raise EntelliwebError("{}: {}".format(data.Error.Code.cdata, data.Error.Message.cdata))
            else:
                log.error(exc)
                log.error(data)
                raise EntelliwebError("UNEXPECTED ERROR!!!")
        try:
            data = data.Row
        except AttributeError as exc:
            raise EntelliwebError("No data found!!!")

        return [{
            'identifier': row.Meter.cdata,
            'timestamp': row.Timeslice.cdata,
            'total': row.Total.cdata,
        } for row in data]

    def meters(self, from_file=None):
        if from_file:
            with open(from_file, 'r') as f:
                data = f.read()
        else:
            response = self.get('meter', headers=headers)
            data = response.text
        return [{
            'identifier': m.ID.cdata,
            'label': m.Name.cdata,
            'description': m.Description.cdata
        } for m in untangle.parse(data).MeterList.Meter]
