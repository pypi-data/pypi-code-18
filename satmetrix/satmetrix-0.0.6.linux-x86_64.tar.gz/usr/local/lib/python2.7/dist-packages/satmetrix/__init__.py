import logging
import json
from urlparse import urlparse, parse_qs

from hammock import Hammock

from .exceptions import SatmetrixAPIErrorInternalError, SatmetrixAPIErrorNotFound, SatmetrixAPIError

def _parse_page_count(url):
    last_qs = parse_qs(urlparse(url).query)
    last = int(last_qs['offset'][0]) + int(last_qs['limit'][0])
    page_count = int(last / int(last_qs['limit'][0]))
    return page_count

def _convert_array_to_dict(array, key):
    data = {}
    for ele in array:
        data[ele[key]] = ele
    return data

class Satmetrix(object):
    def __init__(self, domain, auth):
        url = 'https://{}.satmetrix.com/app/core/v1'.format(domain)
        headers = {'Domain': domain, 'Authorization': 'Basic {}'.format(auth)}
        self.satmetrix = Hammock(url, headers=headers)

    def feedback_record(self, record_id):
        return self.satmetrix.feedback(record_id).GET().json()

    def update_feedback(self, record_id, **kwargs):
        return self.satmetrix.feedback(record_id).PUT(data=json.dumps(kwargs)).json()

    def invitation_record(self, record_id):
        return self.satmetrix.invitations(record_id).GET().json()

    def nominate_contact(self, contact_id=None, **kwargs):
        if contact_id:
            return self.satmetrix.invitations(contact_id).POST(data=json.dumps(kwargs)).json()
        else:
            return self.satmetrix.invitations.POST(data=json.dumps(kwargs)).json()

    def __search_page_of_items(self, _object, offset=0, limit=50, **kwargs):
        params = {'offset': offset, 'limit': limit}
        resp = self.satmetrix(_object)._search.POST(params=params, data=json.dumps(kwargs))
        if resp:

            data = resp.json()
            data['links'] = _convert_array_to_dict(data['links'], 'rel')
            return data

        else:

            if resp.status_code >= 400 and resp.status_code < 500:
                raise SatmetrixAPIErrorNotFound(resp.status_code, resp.url, resp.text)
            elif resp.status_code >= 500 and resp.status_code < 600:
                raise SatmetrixAPIErrorInternalError(resp.status_code, resp.url, resp.text)
            else:
                raise SatmetrixAPIError(resp.status_code, resp.url, resp.text)


    def __search(self, _object, offset=0, limit=50, page_limit=0,
                 callback=None, **kwargs):
        response = []
        
        resp = self.__search_page_of_items(_object, offset, limit, **kwargs)

        if len(resp['data']) > 0:
            if callback:
                response.extend(callback(resp['data']))
            else:
                response.extend(resp['data'])

        if 'next' in resp['links'].keys():
            next = resp['links']['next']['href']
        else:
            next = None

        page_count = _parse_page_count(resp['links']['last']['href'])

        count = 1

        logging.info('Processed %s out of %s pages, added %s rows, next url: %s',
                     count, page_count, len(resp['data']), next)

        while next:
            if page_limit and count >= page_limit:
                return response

            params = parse_qs(urlparse(next).query)

            if 'expand' in params.keys():
                del params['expand']

            params.update(kwargs) # Using one dict instead of 2 to ensure we aren't passing dupolicate arguments.

            resp = self.__search_page_of_items(_object, **params)
            next = resp['links']['next']['href']

            count += 1
            logging.info('Processed %s out of %s pages, added %s rows, next '
                         'url: %s', count, page_count, len(resp['data']), next)

            if len(resp['data']) > 0:
                if callback:
                    response.extend(callback(resp['data']))
                else:
                    response.extend(resp['data'])
            else:
                return response

        return response

    def invitation(self, offset=0, limit=50, page_limit=0, callback=None,
                    **kwargs):
        return self.__search('invitation', offset, limit, page_limit, callback,
                            **kwargs)

    def feedback(self, offset=0, limit=50, page_limit=0, callback=None,
                    **kwargs):
        return self.__search('feedback', offset, limit, page_limit, callback,
                            **kwargs)
