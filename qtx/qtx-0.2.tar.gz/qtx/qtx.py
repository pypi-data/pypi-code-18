import sys
import requests as r
import pandas as pd
from pandas.io.json import json_normalize
import json
import decimal
import apis

base_url = "https://api.quantextive.net"
possible_date_fields = [ 'date', 'entry_date', 'MDEntryDate', 'TradeDate', 'rate_date' ]
possible_time_fields = [ 'MDEntryTime' ]

class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(JsonEncoder, self).default(o)

class Response(object):

    def __init__(self, response):
    	self.response = response

    def json(self):
    	return self.response

    def data_frame(self):
        df = json_normalize(self.response)
        for dateField in possible_date_fields:
            if dateField in df.columns:
                df[dateField] = pd.to_datetime(df[dateField], infer_datetime_format=True)
                sorted = False
                for timeField in possible_time_fields:
                    if timeField in df.columns:
                        df = df.sort_values([dateField, timeField], ascending=False)
                        sorted = True
                if not sorted:
                    df = df.sort_values(dateField, ascending=False)
        return df

class ApiClient(object):

    def __init__(self, default_headers=None):
    	if default_headers is None:
    		default_headers = {}
        self.default_headers = default_headers

    def get(self, api_key, name, params):
        aggr_headers = {}
        aggr_headers.update(self.default_headers)
        
        if api_key != None and api_key != '':
    	    aggr_headers['x-api-key'] = api_key
        
        if 'x-api-key' not in aggr_headers:
            print >> sys.stderr, "API key is required to make a request."
            raise SystemExit
        
        api_found = False
        api_req = None
        if name != None and name != '':
            for request in apis.requests:
                if request['name'] == name:
                    api_found = True
                    api_req = request
                    break
            if not api_found:
                print >> sys.stderr, "API couldn't be found in the available requests " + name
        else:
            print >> sys.stderr, "Error: api name and its params should be supplied"

        if not api_found:
            raise SystemExit

        for param in api_req['params']:
            if param not in params:
                print >> sys.stderr, "Required param missing: --" + param + ', description: ' + api_req['params'][param]
                raise SystemExit

        
        res = r.get(url='/'.join([base_url, name]), params=params, headers=aggr_headers)
        return Response(res.json())