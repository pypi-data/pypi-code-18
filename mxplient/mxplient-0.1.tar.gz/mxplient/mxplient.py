import os
import yaml
import json
import requests
import time
import threading
import uuid
from mxobject import MxObject
from pprint import pprint
from six import string_types
from version import MXVersion


class MXClient(object):

    def __init__(self, url, username=None, password=None, debug=False,
                 anonymous=False, verify=True, offline=False, proxy=None, version=None):
        self.url = url
        self.session = None
        self.verify = verify
        self.debug = debug
        self.version = MXVersion(version) if version else None
        if proxy is not None:
            self.proxies = {'http': proxy, 'https': proxy}
        else:
            self.proxies = None
        self.offline = offline
        if anonymous:
            self.login_anonymous()
        else:
            self.login(username, password)

    def login(self, username, password):
        login_action = {
            'action': 'login',
            'params': {},
        }
        if username and password:
            login_action['params']['username'] = username
            login_action['params']['password'] = password

        self.username = username
        self.password = password

        (response, code) = self.request(login_action)
        if code != 200:
            raise Exception("Login failed: " + str(response))

        keepalive = KeepAlive(self)
        keepalive.daemon = True
        keepalive.start()

    def logout(self):
        logout_action = {
            'action': 'logout',
            'params': {},
        }

        (response, code) = self.request(logout_action)
        if code != 200:
            raise Exception("Logout failed: " + str(response))

    def login_anonymous(self):
        get_session_data_action = {
            'action': 'get_session_data',
            'params': {
                'profile': '',
                'timezoneoffset': -60,
            }
        }

        if self.offline:
            get_session_data_action['params']['offline'] = True
            get_session_data_action['params']['profile'] = 'phone'

        (response, code) = self.request(get_session_data_action)

        if 'sync_config' in response.keys():
            self.sync_config = response['sync_config']

        if code != 200:
            raise Exception("Getting anonymous session failed: " + str(response))

    def relogin(self):
        self.login(self.username, self.password)

    def keepalive(self):
        return self.request({"action": "keepalive"})

    def request(self, request, request_id=True):
        if request_id is True:  # false -> omit header, str -> specify req_id
            request_id = str(uuid.uuid4())

        if not self.session:
            self.session = requests.Session()

        if self.debug:
            pprint(request)

        headers = {'Content-Type': 'application/json'}
        if request_id:
            headers['X-Mx-ReqToken'] = request_id

        response = self.session.post(
            self.url,
            data=json.dumps(request),
            headers=headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response.raise_for_status()
        response_body = json.loads(response.text)
        if self.debug:
            pprint(response_body)
        if 'csrftoken' in response_body:
            self.session.headers.update({
                'X-Csrf-Token': response_body['csrftoken']
            })
        return (response_body, response.status_code)

    def download(self, entity, file_path):
        if not self.session:
            self.session = requests.Session()

        url = "%s/file?guid=%s" % (
            '/'.join(self.url.split("/")[0:3]), entity.guid
        )
        with open(file_path, 'wb') as handle:
            response = self.session.get(url,
                                        verify=self.verify,
                                        proxies=self.proxies,
                                        stream=True)

            if not response.ok:
                print "argh: %s" % response

            for block in response.iter_content(1024):
                handle.write(block)

    def upload(self, entity, file_path):
        file_url = "%s/file?guid=%s" % (
            '/'.join(self.url.split("/")[0:3]), entity.guid
        )
        if not self.session:
            self.session = requests.Session()
        basename = os.path.basename(file_path)
        if not self.version or self.version < 6.7:
            files = {basename: open(file_path, 'rb')}
        elif self.version < 7:
            files = {
                "changes": "{}",
                "mxdocument": (basename, open(file_path, 'rb'))
            }
        else:
            files = {
                "data": "{objects: [], changes: {}",
                "blob": (basename, open(file_path, 'rb'))
            }
        response = self.session.post(
            file_url,
            files=files,
            verify=self.verify,
            proxies=self.proxies,
            headers={"Accept": "application/json"}
        )
        if self.debug:
            pprint({
                'method': 'upload',
                'request': {
                    'url': file_url,
                    'path': file_path,
                },
                'response': response.text
            })
        return (response.text, response.status_code)

    def xpath_request(self, xpath, count=None, offset=None, schema_id=None,
                      attributes=None):
        amount = 0
        if count is None:
            count = False
        else:
            amount = count
            count = True
        if offset is None:
            offset = 0
        request = {
            "action": "retrieve_by_xpath",
            "params": {
                "xpath": xpath,
                "schema": {
                    "amount": amount,
                    "offset": offset,
                },
                "count": count,
                "aggregates": False
            },
            "context": [],
        }
        if schema_id is not None:
            request['params']['schema']['id'] = schema_id
        if attributes is not None:
            request['params']['schema']['attributes'] = attributes
        return self.request(request)

    def vulnerability_report(self, elaborate=False):
        session_data = self.get_session_data()
        print 'app:', self.url
        print 'username:', self.username
        print 'roles:', ' '.join(map(lambda x: str(x['attributes']['Name']['value']), session_data['roles']))
        print ''
        for entity in session_data['metadata']:
            self._vulnerability_report_for_entity(entity, elaborate)

    def _vulnerability_report_for_entity(self, entity, elaborate=False):
        entity_name = entity['objectType']
        try:
            count = self.xpath_request('//' + entity_name, 1, 0)[0]['count']
        except:
            #  non persistent entities don't allow xpath
            count = 0
        print '-------------------------------'
        print 'entity:', entity_name
        print 'attributes:'
        attributes = sorted(map(str, entity['attributes'].keys()))
        for attribute in attributes:
            print '-', attribute
        print 'visible objects', count
        if elaborate:
            print '\t'.join(attributes)
            for object in self.get_objects_by_xpath_iterator('//' + entity_name):
                print '\t'.join(map(str, (object.object['attributes'][key]['value'] for key in attributes)))

    def xpath_request_with_schema(self, xpath, offset, limit, sort):
        return self.request({
            "action": "retrieve_by_xpath",
            "params": {
                "xpath": xpath,
                "schema": {
                    "offset": offset,
                    "amount": limit,
                    "sort": sort,
                },
                "count": False,
                "aggregates": False
            },
            "context": [],
        })

    def get_microflow(self, mxf_path, caption=None):
        response = self.session.get(
            self.url.replace("xas/", "forms/en_US/%s" % mxf_path),
            verify=self.verify,
            proxies=self.proxies,
        )
        if response.status_code == 404:
            response = self.session.get(
                self.url.replace("xas/", "pages/en_US/%s" % mxf_path),
                verify=self.verify,
                proxies=self.proxies,
            )
        import string
        cleaned = filter(lambda x: x in string.printable, response.text)
        import relaxml
        body = relaxml.xml(cleaned)
        mx4 = self._retrieve_actionname_from_form(body)
        if mx4 is not None:
            return mx4
        else:
            return self._find_microflow_in_page(body, caption)

    def _retrieve_actionname_from_form(self, mxform):
        result = None
        for key in mxform.keys():
            value = mxform[key]
            if isinstance(key, tuple):
                if "actionname" in key:
                    return value
            if isinstance(value, dict):
                result = self._retrieve_actionname_from_form(value)
                if result is not None:
                    return result
            elif isinstance(value, list):
                for child in value:
                    result = self._retrieve_actionname_from_form(child)
                    if result is not None:
                        return result
        return result

    def _find_microflow_in_page(self, tree, caption=None):
        result = None
        if not isinstance(tree, dict):
            return None

        for value in tree.values():
            if isinstance(value, dict):
                result = self._find_microflow_in_page(value, caption)
                if result is not None:
                    return result
            elif isinstance(value, list):
                for i in value:
                    result = self._find_microflow_in_page(i, caption)
                    if result is not None:
                        return result
            elif isinstance(value, str):
                temp_string = '{%s}' % value
                try:
                    temp = json.loads(temp_string)
                except ValueError:
                    continue
                microflow_name = None
                try:
                    # FIXME: 
                    # Mendix version 5.something.late has action in the json.
                    # We could also switch to something smart like json.
                    if 'action' in temp:
                        microflow_name = temp['action']['microflow']['name']
                    else:
                        microflow_name = temp['microflow']['name']

                    if temp['caption'] == caption or caption is None:
                        return microflow_name
                except KeyError:
                    pass
        return result

    def get_session_data(self):
        data, status_code = self.request({
            "action": "get_session_data",
            "params": {
                "timezoneoffset": 0,
                "profile": "",
            },
        })
        if status_code != 200:
            raise Exception("Could not get session data, result: %s" % data)
        return data

    def get_objects_by_path(self, path, guid):
        jsonobject, status_code = self.request({
            'action': 'retrieve_by_path',
            'params': {
                'id': _get_guids(guid)[0],
                'path': path,
            },
            'context': [],
        })
        if status_code != 200:
            raise Exception("get objects by path failed, result: %s" % jsonobject)
        return self._get_mxobjects(jsonobject)

    def get_objects_by_xpath(self, xpath, attributes=None):
        (result, status_code) = self.xpath_request(xpath, attributes=attributes)
        if status_code != 200:
            raise Exception("xpath failed, result: %s" % result)

        return self._get_mxobjects(result)

    def get_objects_by_xpath_iterator(self, xpath, schema_id=None, attributes=None):
        offset = 0
        while True:
            (result, status_code) = self.xpath_request(xpath, count=20, offset=offset, schema_id=schema_id, attributes=attributes)
            if status_code != 200:
                raise Exception("xpath failed, result: %s" % result)
            results = self._get_mxobjects(result)
            for obj in results:
                yield obj
            if len(results) == 0:
                break
            offset += 20

    def get_objects_by_xpath_with_schema(self, xpath, offset, limit, sort):
        (result, status_code) = self.xpath_request_with_schema(xpath, offset, limit, sort)
        if status_code != 200:
            raise Exception("xpath failed, result: %s" % result)

        return self._get_mxobjects(result)

    def get_object_by_guid(self, entity_path, guid):
        print("get_object_by_guid is deprecated, use get_objects_by_ids")
        objects = self.get_objects_by_xpath("//%s[id = '%s']" % (
            entity_path, guid
        ))
        if len(objects) != 1:
            raise Exception("Failed to retrieve object '%s' from '%s'" % (
                guid, entity_path
            ))
        return objects[0]

    def get_objects_by_ids(self, guids, attributes=None):
        request = {
            'action': 'retrieve_by_ids',
            'params': {
                'ids': _get_guids(guids),
                'schema': {},
            },
            'context': [],
        }
        if attributes is not None:
            request['params']['schema']['attributes'] = attributes
        jsonobject, status_code = self.request(request)
        if status_code != 200:
            raise Exception("get objects by id failed, result: %s" % jsonobject)
        return self._get_mxobjects(jsonobject)

    def execute_microflow(self, name, params=None, context=None,
                          instruction_filter=None, request_id=True,
                          applyto='selection'):
        body, status_code = self._execute_microflow(name, params,
                                                    context, request_id,
                                                    applyto)

        action = None
        if 'instructions' not in body:
            pass
        elif instruction_filter is None:
            try:
                action = body['instructions'][0]
            except IndexError:
                pass
        else:
            for instruction in body['instructions']:
                if instruction['type'] == instruction_filter:
                    action = instruction
        if action:
            form_guid = _get_form_guid(action)
            mxf_path = _get_mxf_path(action)
            args = _get_args(action)
            return (args, mxf_path, form_guid)
        return (None, None, None)

    def execute_microflow_response(self, name, params=None, context=None):
        body, status_code = self._execute_microflow(name, params, context)

        if status_code == 560 and body['type'] == 'exception':
            raise MicroflowExecutionException(body['description'])

        return MxResponse(body)

    def instantiate(self, entity_name):
        jsonobject, status_code = self.request({
            "action": "instantiate",
            "params": {"objecttype": entity_name},
            "context": []
        })
        if status_code != 200:
            raise Exception("instantiate object failed, result: %s" % jsonobject)
        return self._get_mxobject(jsonobject)

    def delete_object(self, guid):
        return self.request({
            "action": "delete",
            "params": {"guids": [guid]},
            "context": []
        })

    def change_object(self, obj, attribute, value):
        request = {
            "action": "change",
            "params": {
                obj.guid: {attribute: value}
            },
            "context": []
        }
        return self.request(request)

    def commit_object(self, obj):
        request = {
            "action": "commit",
            "params": {"guid": obj.guid},
            "context": []
        }
        return self.request(request)

    def _get_mxobject(self, xas_result):
        if not self.version or self.version < 7:
            return MxObject(xas_result['mxobject'], self)
        return MxObject(xas_result['objects'][0], self)

    def _get_mxobjects(self, xas_result):
        if not self.version or self.version < 7:
            return [MxObject(obj, self) for obj in xas_result['mxobjects']]
        return [MxObject(obj, self) for obj in xas_result['objects']]

    def _execute_microflow(self, name, params=None, context=None, request_id=True,
                           applyto='selection'):
        guids = [] if params is None else _get_guids(params)
        request = {
            'action': 'executeaction',
            'params': {
                'applyto': applyto,
                'actionname': str(name),
                'guids': guids,
            }
        }
        if context:
            request['context'] = _get_guids(context)
        (body, status_code) = self.request(request, request_id=request_id)
        if self.debug:
            pprint({
                'method': 'execute_microflow',
                'request': request,
                'response': {
                    'body': body,
                    'status_code': status_code
                }
            })

        return body, status_code


class MxResponse(object):

    def __init__(self, body):
        self.messages = []
        self.forms = []
        self.body = body
        try:
            self.guid = body['actionResult']['guid']
        except:
            self.guid = None
        if 'instructions' not in body:
            return
        for instruction in body['instructions']:
            if instruction['type'] == 'open_form':
                self.forms.append((
                    instruction['args']['FormGuid'],
                    instruction['args']['FormPath'],
                    instruction['args'],
                ))
            elif instruction['type'] == 'text_message':
                self.messages.append((
                    instruction['args']['MessageContent'],
                    instruction['args']['MessageType'],
                    instruction['args'],
                ))

        self._check_for_errors()

    def _check_for_errors(self):
        messages = self.messages[:]
        while len(messages) > 0:
            message = messages.pop()
            if message[1] == 'ERROR':
                raise MicroflowExecutionException(message[2])

    def _get_first(self, l):
        if l:
            return l[0]
        else:
            return None

    def get_first_form(self):
        return self._get_first(self.forms)

    def get_first_close_form(self):
        return self._get_first(self.close_forms)

    def get_first_message(self):
        return self._get_first(self.messages)

    def get_guid(self):
        return self.guid

    def get_first_form_guid(self):
        if len(self.forms) > 0:
            f = self._get_first(self.forms)
            if f:
                return f[0]
        return None


class MicroflowExecutionException(Exception):
    pass


def _get_form_guid(action):
    try:
        form_guid = action['args']['FormGuid']
    except KeyError:
        form_guid = None
    return form_guid


def _get_guids(param):
    if param is None:
        raise Exception("_get_guids param is None")
    res = None
    if isinstance(param, string_types):
        res = [param]
    else:
        try:
            res = [p for p in param]
        except TypeError:
            res = [param]
    return [str(x.guid) if isinstance(x, MxObject) else str(x) for x in res]


def _get_mxf_path(action):
    try:
        mxf_path = action['args']['FormPath']
    except KeyError:
        mxf_path = None
    return mxf_path


def _get_args(action):
    try:
        args = action['args']
    except KeyError:
        args = None
    return args


def _load_config(config_path):
    config = {}
    config_files = [config_path, 'mxplient.yaml']
    mxplient_yaml = None
    for config_file in config_files:
        config_file_expanded = os.path.expanduser(config_file)
        if os.path.exists(config_file_expanded):
            mxplient_yaml = config_file_expanded
            break
    if mxplient_yaml is not None:
        with open(mxplient_yaml) as yaml_file:
            config = yaml.load(yaml_file)
    else:
        raise Exception('No config passed as arg and %s doesnt exist' % config_path)
    return config


def load_client(config_path='~/.mxplient/mxplient.yaml', app_name=None, user=None, password=None):
    config = _load_config(config_path)
    app_config = config
    if app_name:
        app_config = config[app_name]
    xas_url = app_config['url']
    if user is None:
        user = app_config['user']
        password = app_config['password']
    proxy = app_config.get('proxy', None)
    verify = app_config.get('ca_bundle', None)
    return MXClient(
        xas_url,
        user,
        password,
        proxy=proxy,
        verify=verify,
    )


def list_users(client):
    objects = client.get_objects_by_xpath("//Administration.Account")
    for node in objects:
        print node.RealEmailaddress


class KeepAlive(threading.Thread):
    def __init__(self, plient):
        super(KeepAlive, self).__init__()
        self.plient = plient

    def run(self):
        while True:
            try:
                body, status = self.plient.keepalive()
                if status != 200:
                    break
            except:
                pass
            time.sleep(30)
