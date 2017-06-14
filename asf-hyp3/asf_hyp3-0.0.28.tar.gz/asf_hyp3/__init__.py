# hy3-module.py
# William Horn, Hal DiMarchi, Rohan Weeden
# Created: May 31, 2017
# Class to interface with the API

import json
import re

import requests
import shapefile
import pygeoif

import getpass
import base64

try:
    # Python 2.x Libs
    from urllib2 import build_opener, install_opener, Request, urlopen, HTTPError
    from urllib2 import URLError, HTTPHandler, HTTPRedirectHandler, HTTPCookieProcessor
    from urllib import addinfourl

    from cookielib import CookieJar
    from StringIO import StringIO

except ImportError:
    # Python 3.x Libs
    from urllib.request import build_opener, install_opener, Request, urlopen
    from urllib.request import HTTPHandler, HTTPRedirectHandler, HTTPCookieProcessor
    from urllib.response import addinfourl
    from urllib.error import HTTPError, URLError

    from http.cookiejar import CookieJar
    from io import StringIO

if __name__ == "__main__":
    from scripts import _granule_pattern as granule_pattern
    from scripts import load_granules
else:
    from .scripts import _granule_pattern as granule_pattern
    from .scripts import load_granules
"""
    |************************* API CLASS *************************************|

   Works with the hyp3-api and does all the get requests as well as saving
   the repeated data between class, like the username and api_key.

   formats: json by default which will be converted into appropriate data type,
            csv or any orther format returns string of data recieved

   functions are:
       get_jobs: returns a list of dictionaries or a string depending on format
       get_job: returns a dictionaryf
       get_products: returns a list of dictionaries or a string depending on format
       get_process: return a dictionary or a string depending on format
       get_processes: returns a list of dictionaries or a string depending on format
       one_time_process: returns a dictionary

       get_subscriptions: return a list of dictionaries or a string depending on format
       create_subscription: returns a dictionary
       remove_subscription: returns a dictionary
       enable_subscription: returns a dictionary
       disable_subscription: returns a dictionary

       go to https://api.hyp3.asf.alaska.edu/ for further documentation

       from asf_hyp3_api import api
"""


class API:
    url = ""
    username = ""
    api_key = ""

    _pair = "requires pair"
    _dual = "requires dual pol"

    # processes that require a pair of granules
    _pair_req = {6: _pair, 7: _pair,
                 8: _pair, 10: _pair,
                 13: _pair, 17: _pair}
    # processes that require dual polarization
    _dual_pol_req = {12: _dual, 13: _dual}

    # Constructor, set url, username and api_key, if no password or api_key
    # is given will prompt the user for earthdata username and password and
    # attempt to login
    def __init__(self, username, password=None, api_key=None, url="https://api.hyp3.asf.alaska.edu/"):
        self.url = url

        # check to see if the url is valid and can connect
        try:
            requests.get(self.url)
        except requests.exceptions.ConnectionError as connectError:
            print(str(connectError))
        except:
            print("In API::__init__ - Error in url '{}' or connection to server ".format(self.url))

        self.username = username
        self.api_key = api_key

    # Returns a dictionary of the parameters used in every function
    def _get_default_args(self):
        if self.api_key is None:
            raise StandardError(
                "in API::_get_default_args - api_key not set call .login() to get credentials")
        return {"username": self.username, "api_key": self.api_key}

    # Returns either a dictionary if format is json or a string in csv format
    # depending on the format variable
    #      Exception if the format is not recognized
    def _formatter(self, data, format=None):
        formatted_data = ""

        if format == "json" or format is None:
            try:
                formatted_data = json.loads(data)
            except:
                formatted_data = data
        else:
            # Data is already in a string in csv format from server
            formatted_data = data

        return formatted_data

    # Check if a granule string is dual_pol
    def _isDualPol(self, granule):
        pol = granule[14]
        return pol == "D"

    def _make_request(self, func_name, args, format):
        req_args = self._get_default_args()
        # Only put the arguments into the url if the value is passed to the function
        req_args.update({key: value for (key, value) in args.items() if value is not None})
        url = self.url + func_name
        # make the request to the server
        text = requests.get(url, req_args).text
        # return either a json dictionary or a csv string
        return self._formatter(text, format)

    # Getters an setters for class attributes
    def get_username(self):
        return self.username

    def set_username(self, new_username):
        self.username = new_username

    def get_api_key(self):
        return self.api_key

    def set_api_key(self, new_api_key):
        self.api_key = new_api_key

    def get_url(self):
        return self.url

    def set_url(self, new_url):
        self.url = new_url

    """Logs the user in and gets a valid api key"""

    def login(self, password=None):

        edlogin = EarthdataLogin("YsS6RMIBT4s10UJzyejGaQ", self.url + "login/authorized")

        if password is None:
            new_password = getpass.getpass(prompt="Password for {}: ".format(self.username))
        else:
            new_password = password
        session_cookie, response = edlogin.getLoginCookie(self.username, new_password)

        resp = json.loads(response.read())
        if 'api_key' in resp:
            self.api_key = resp['api_key']
        elif 'status' in resp and resp['status'] == "ERROR":
            print("New users: you must first log into the Hyp3 Api (and Hyp3 if you have not done so already)")
            print("Hyp3 Api: " + self.url + "login")
            print("Hyp3: http://hyp3.asf.alaska.edu/login")
            exit(-1)
        else:
            key_resp = json.loads(requests.get(self.url + "reset_api_key",
                                               cookies={session_cookie.name: session_cookie.value}).text)

            if 'api_key' in key_resp:
                self.api_key = key_resp['api_key']
            elif 'message' in key_resp:
                print("Error: " + key_resp['message'])
            else:
                print("An error occurred")
                exit(-1)

    """Returns a list of dictionaries containing job information with the specified attributes.
       Job info:
            - id, sub_id, user_id, process_id, status, granule,
              granule_url, other_granules, other_granule_urls,
              request_time, processed_time, priority, message
    """

    def get_jobs(self,
                 id=None,
                 status=None,
                 sub_id=None,
                 granule=None,
                 format=None):
        # Required parameters
        args = self._get_default_args()

        # always make the format lowercase
        if format is not None:
            format = format.lower()

        optional_args = {"id": id,
                         "status": status,
                         "sub_id": sub_id,
                         "granule": granule,
                         "format": format}
        args.update({key: value for (key, value) in optional_args.items() if value is not None})

        # url for the get call
        get_jobs_url = self.url + "get_jobs"

        # checks to see if the id arg is a list
        if isinstance(id, list):
            # saves the ids as a set
            ids = set(args['id'])

            # Get all the jobs
            args.pop('id', None)
            all_jobs = requests.get(get_jobs_url, args).text

            # make sure the format is correct
            if format is not None and format.lower() == "csv":
                raise StandardError(
                    "In API::get_jobs - csv format not supported with list selection on id")

            # format he data
            all_jobs = self._formatter(all_jobs, format)

            jobs = []
            # looks through all the jobs returned and filters by id
            for job in all_jobs:
                if job['id'] in ids:
                    jobs.append(job.copy())

            # return either a list of json dictionaries
            return jobs

        else:
            jobs = requests.get(get_jobs_url, args).text
            # return either a list of json dictionaries or a csv string
            return self._formatter(jobs, format)

    """Returns a dictionary just like the one referenced in get_jobs"""

    def get_job(self, id, format=None):
        job = self.get_jobs(id=id, format=format)

        if isinstance(job, list) and len(job) > 0:
            # strips off the list around the dictionary
            return job[0]
        else:
            # Most likely there was an error/ or an empty list
            return job

    """Returns a list of dictionaries product information with the specified
       attributes.
    Product info contains fields:
        - id, sub_id, name, url, browse_url,
          size, creation_date
    """

    def get_products(self,
                     id=None,
                     sub_id=None,
                     sub_name=None,
                     creation_date=None,
                     name=None,
                     format=None):
        # always make the format lowercase
        if format is not None:
            format = format.lower()

        args = {"id": id,
                "sub_id": sub_id,
                "sub_name": sub_name,
                "creation_date": creation_date,
                "name": name,
                "format": format}

        return self._make_request('get_products', args, format)

    """Returns a dictionary just like the one referenced in get_product"""

    def get_product(self, id, format=None):
        product = self.get_products(id=id, format=format)

        if isinstance(product, list) and len(product) > 0:
            # strips off the list around the dictionary
            return product[0]
        else:
            return product
            # Most likely there was an error

    """Returns a dictionary or a string depending on format containing information about the process.
        return fields are:

        - id, name, description, requires_pair,
          supports_time_series_processing, requires_dual_pol
    """

    def get_process(self, id, format=None):
        # Required args
        args = {"id": id}

        # always make the format lowercase
        if format is not None:
            format = format.lower()
            args["format"] = format

        return self._make_request('get_process', args, format)

    """Returns a list of dictionaries all available processes. Each entry is as
       described by get_process.
    """

    def get_processes(self, format=None):
        # always make the format lowercase
        args = {}
        if format is not None:
            format = format.lower()
            args = {'format': format}

        return self._make_request('get_processes', args, format)

    """Schedules a new processing request and returns a dictionary
       indicating whether or not the request succeeded, and an error message.
       If the process_id specifies a process that requires a granule pair,
       then other_granules must also be supplied.

       The granule can be either passed as a string or as the path of the file that
       contains the granule(s)
    Returns:
        {"status": "SUCCESS", "message": null} or
        {"status": "SUCCESS", "id": 8000}
    """

    def one_time_process(self,
                         granule,
                         process_id,
                         other_granule=None,
                         priority=None,
                         message=None):
        granules = None
        # all the required args for function
        args = self._get_default_args()

        # Checks for a list of granules
        if isinstance(granule, list):
            granules = granule
            for g in granules:
                # Make sure all are valid granule string
                if not re.search(granule_pattern, g):
                    raise StandardError(
                        "in API::one_time_process - Invalid Granule Passed: {}".format(g))
                # Check if the processes is compatible
                if process_id in self._pair_req and other_granule is None:
                    raise StandardError(
                        "API::one_time_process - Process_id given requires a pair of granules")
                if process_id in self._dual_pol_req and not self._isDualPol(g):
                    raise StandardError(
                        "API::one_time_process - Process_id given requires a granule with dual_pol")

        # Checks to see if the string is not a granule
        elif isinstance(granule, str) and (not re.search(granule_pattern, granule) and not isinstance(granule, list)):
            path = granule
            granules = load_granules(path)
        # Check if its an open file...
        elif isinstance(granule, file):
            granules = load_granules(granule)
        else:
            # Granule should just be a regular granule string
            granule = granule

        if granules is not None and isinstance(process_id, list):
            if not len(process_id) == len(granules):
                raise StandardError(
                    "API::one_time_process - Process_id given requires a pair of granules")

        args.update({"granule": granule, "process_id": process_id})

        optional_args = {"other_granules": other_granule,
                         "priority": priority,
                         "message": message}

        # doesn't add optional parameters that haven't been entered
        args.update({key: value for (key, value) in optional_args.items() if value is not None})

        if process_id in self._pair_req and other_granule is None:
            raise StandardError(
                "API::one_time_process - Process_id given requires a pair of granules")
        if process_id in self._dual_pol_req and not self._isDualPol(granule):
            raise StandardError(
                "API::one_time_process - Process_id given requires a granule with dual_pol")

        url = self.url + "one_time_process"

        # If there is a list either from a file or passed directly
        if granules is not None:
            statuses = []

            for g in granules:
                args['granule'] = g

                status = requests.get(url, args)
                status = json.loads(status.text)

                statuses.append(status)

            return statuses

        # Otherwise just a single granule
        else:
            status = requests.get(url, args)

        return json.loads(status.text)

    def one_time_process_batch(self, filename):
        args = self._get_default_args()
        files = {'file': open(filename)}
        response = requests.post(self.url + "one_time_process_batch", params=args, files=files)
        return self._formatter(response.text, 'json')

    """Schedules a new subscription and returns a dictionary indicating
       whether or not the request succeeded, as well as an error message in
       the event of failure.
    """

    def create_subscription(self,
                            crop_to_selection,
                            name,
                            process_id,
                            platform,
                            location,
                            polarization='{}',
                            start_date=None,
                            end_date=None,
                            description=None,
                            extra_arguments="no",
                            enable=True,
                            project_id=None):
        # All the required parameters
        args = self._get_default_args()
        args.update({"polarization": polarization,
                     "crop_to_selection": str(crop_to_selection),
                     "name": name,
                     "process_id": str(process_id),
                     "platform": platform})

        if not re.match("MULTIPOLYGON", location) and not (re.match(".(dbf|prj|shp|shx)", location)):
            try:
                sf = shapefile.Reader(location)
            except Exception as e:
                return "Error loading files: Ensure you have both necessary files (.dbf and .shp) present in the directory of the file path you passed and note: " + str(e)

            shape = []
            for feature in sf.shapes():
                shape.append(pygeoif.geometry.as_shape(feature))
            location = pygeoif.MultiPolygon(shape).wkt

        optional_args = {"location": location,
                         "start_date": start_date,
                         "end_date": end_date,
                         "description": description,
                         "extra_arguments": extra_arguments,
                         "enable": enable,
                         "project_id": project_id}

        # doesn't add optional parameters that haven't been entered
        args.update({key: value for (key, value) in optional_args.items() if value is not None})

        url = self.url + "create_subscription"
        new_subscription = requests.get(url, args).text

        return new_subscription

        return json.loads(new_subscription)

    """Returns a array of subscription information with the specified
       attributes or a string depending on format. Subscription info contains fields:

        - id, process_id, user_id, name, location,
          start_date, end_date, enabled
    """

    def get_subscriptions(self,
                          id=None,
                          process_id=None,
                          name=None,
                          location=None,
                          start_date=None,
                          end_date=None,
                          enabled=None,
                          format=None,
                          project_id=None):

        # always make the format lowercase
        if format is not None:
            format = format.lower()

        args = {"id": id,
                "process_id": process_id,
                "name": name,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "enabled": enabled,
                "format": format,
                "project_id": project_id}

        return self._make_request('get_subscriptions', args, format)

    """Returns a dictionary just like the one referenced in get_subscriptions"""

    def get_subscription(self, id, format=None):
        subscription = self.get_subscriptions(id=id, format=format)

        if isinstance(subscription, list) and len(subscription) > 0:
            # strips off the list around the dictionary
            return subscription[0]
        else:
            # Most likely there was an error
            return subscription

    """Sets the property 'enabled' of a subscription to False. No further
       actions will be taken based on this subscription until it is enabled
       again. Returns a dictionary indicating whether or not the request
       succeeded, and an error message in the event it did not.
    """

    def disable_subscription(self, sub_id, project_id=None):
        args = self._get_default_args()
        args['sub_id'] = sub_id
        if project_id:
            args['project_id'] = project_id

        url = self.url + "disable_subscription"
        sub_status = requests.get(url, args)

        return json.loads(sub_status.text)

    def enable_subscription(self, sub_id, project_id=None):
        args = self._get_default_args()
        args['sub_id'] = sub_id
        if project_id:
            args['project_id'] = project_id

        url = self.url + "enable_subscription"
        sub_status = requests.get(url, args)

        return json.loads(sub_status.text)

    def is_granule(self, obj):
        pattern = re.compile(
            r'(S1[A-D]_(IW|EW|WV|S1|S2|S3|S4|S5|S6)_(GRD|SLC|OCN)[FHM_]_[12][SA](SH|SV|DH|DV)_\d{8}T\d{6}_\d{8}T\d{6}_\d{6}_[0-9A-F]{6}_[0-9A-F]{4})')
        if isinstance(obj, str):
            if re.search(pattern, obj):
                return True
        return False

# |---------------------- END API CLASS -------------------------|


class EarthdataLogin(object):
    def __init__(self, client_id, redirect_url):
        self.urls = {'url': 'https://urs.earthdata.nasa.gov/oauth/authorize',
                     'client': client_id,
                     'redir': redirect_url}

    def getLoginCookie(self, username, password):
        url = '{0}?response_type=code&client_id={1}&redirect_uri={2}'.format(
            self.urls['url'], self.urls['client'], self.urls['redir'])
        user_pass = self.httpBasicAuth(username, password)
        # Authenticate against URS, grab all the cookies
        cj = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
        request = Request(url, headers={"Authorization": "Basic {0}".format(user_pass)})

        # Watch out cookie rejection!
        try:
            response = opener.open(request)
        except HTTPError as e:
            if e.code == 401:
                print (" > Username and Password combo was not successful. Please try again.")
                return None
            else:
                # If an error happens here, the user most likely has not confirmed EULA.
                print ("\nIMPORTANT: There was an error obtaining a download cookie!")
                print ("\n\nNew users: you must first log into Hyp3 and accept the EULA. In addition, your Study Area must be set at Earthdata https://urs.earthdata.nasa.gov")
                exit(-1)
        except URLError as e:
            print ("\nIMPORTANT: There was a problem communicating with URS, unable to obtain cookie. ")
            print ("Try cookie generation later.")
            exit(-1)

        session_cookie = None
        for cookie in cj:
            if cookie.name == "session":
                session_cookie = cookie
                break

        return session_cookie, response

    def httpBasicAuth(self, username, password):
        try:
            # python2
            user_pass = base64.b64encode(bytes(username + ":" + password))
        except TypeError:
            # python3
            user_pass = base64.b64encode(bytes(username + ":" + password, "utf-8"))
            user_pass = user_pass.decode("utf-8")
        return user_pass


def function_tester(func, args, doesPrint=True):
    print("|-------- TESTING {} -------|".format(func.__name__))
    data = func(*args)
    if doesPrint:
        print(data)


def function_format_tester(func, format, doesPrint=True):
    print("|-------- TESTING {} (CSV)-------|".format(func.__name__))
    data = func(format=format)
    if doesPrint:
        print(data)


# test all the subscription and processes functions
def __test_job_processes(test, doesPrint=True):

    # test get_processes
    print("|-------- TESTING {} -------|".format("get_processes"))
    processes = test.get_processes()
    print(processes)

    # test the get_process function
    print("|-------- TESTING {} -------|".format("get_process"))
    process_id = 2
    process_info = test.get_process(process_id)
    print(process_info)

    # test the get_jobs function, prints out a json string
    print("|-------- TESTING {} -------|".format("get_process"))
    jobs = test.get_jobs()
    print("Total jobs : {}".format(len(jobs)))

    print("|-------- TESTING one_time_process -------|")
    granule = "S1A_IW_SLC__1SSV_20150127T095630_20150127T095657_004355_005505_7518"
    status = test.one_time_process(granule, process_id, priority=5, message="Hello thar!")
    print(status)

    # test the get_products function
    print("|-------- TESTING {} -------|".format("get_products"))
    products = test.get_products()
    print(products)


def __demo(interface):
    num_processes = len(interface.get_processes())

    # makes a list with half the names Hal and half the name Will
    names = ["Hal" if (index < num_processes / 2) else "Will" for name,
             index in enumerate(range(num_processes))]

    # Creates a subscription for every processes
    for process, name in zip(interface.get_processes(), names):
        process_id = process['id']
        status = interface.create_subscription('{"VV"}', "False", name, str(
            process_id), "sentinel-1a", location="MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), (30 20, 20 15, 20 25, 30 20)))", extra_arguments="no")
        sub_id, name = status["id"], process["name"]
        print("Adding subscription: {}, with process: {}". format(process_id, name))

    # print all the subscriptions with hal as the name
    for sub in interface.get_subscriptions(name="Will"):
        sub_id, name = sub['id'], sub['name']
        print("subscription: {}, Name: {}").format(sub_id, name)

    # remove all the subscriptions
    for sub in interface.get_subscriptions():
        sub_id = sub["id"]
        print("removing subscription {}".format(sub_id))
        interface.remove_subscription(sub_id)

    print("Subscriptions remaining: {}".format(len(interface.get_subscriptions())))


def __test_subscriptions(test, doesPrint=True):
    # test the create_subscriptions function
    print("|-------- TESTING create_subscriptions -------|")
    crop_to_selection, name, process_id, platform = False, "Hal", 7, "sentinel-1a"
    location = "MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40))," \
        "((20 35, 10 30, 10 10, 30 5, 45 20, 20 35)," \
        "(30 20, 20 15, 20 25, 30 20)))"

    new_sub = test.create_subscription(crop_to_selection, name, process_id, platform,
                                       location, extra_arguments="no")
    if doesPrint:
        print(new_sub)
    sub_id = new_sub["id"]

    # test the get_subscriptions function
    print("|-------- TESTING get_subscriptions -------|")
    subs = test.get_subscriptions()
    print(subs)

    # test the disable_subscription function
    print("|-------- TESTING disable_subscriptions -------|")
    status = test.disable_subscription(sub_id)
    print(status)

    # test the enable_subscription function
    print("|-------- TESTING enable_subscriptions -------|")
    status = test.enable_subscription(sub_id)
    print(status)


def __test_formats(test, doesPrint=True):
    # test csv format on the get_subscriptions function
    function_format_tester(test.get_subscriptions, "CsV")

    # test csv format on the get_jobs function
    function_format_tester(test.get_jobs, "csV")

    # test csv format on the get_processes function
    function_format_tester(test.get_processes, "CsV")


def __test_range_id_select(interface):
    jobs = interface.get_jobs(id=range(8520, 8531))

    print("Selected jobs:")
    for job in jobs:
        print("\tjob id - {}".format(job['id']))


def __test_one_time_processes(interface):
    print("|-------- TESTING one granule string -------|")
    granule = "S1A_IW_SLC__1SSV_20150127T095630_20150127T095657_004355_005505_7518"
    status = interface.one_time_process(granule, 2, priority=5, message="Hello thar!")
    print(status)

    print("|-------- TESTING list of granule strings -------|")
    granules = ["S1A_IW_GRDH_1SDV_20150324T013037_20150324T013102_005167_00683D_92A3",
                "S1A_IW_SLC__1SSV_20150127T095630_20150127T095657_004355_005505_7518",
                "S1A_IW_SLC__1SSV_20150127T095630_20150127T095657_004355_005505_7518"]

    other_gran = 'S1A_IW_GRDH_1SDV_20150324T013102_20150324T013138_005167_00683D_B814'

    status = interface.one_time_process(
        granules, 6, other_granules=other_gran, priority=5, message="Hello thar!")
    print(status)

    # print("|-------- TESTING path to granule file -------|")
    # path = "/home/william/hyp3-api/asf-datapool-results-2017-6-6_10-25-45.csv"
    # status = interface.one_time_process(path, 2, priority=5, message="Hello thar!")
    # print(status)


def __test_all(interface):
    __test_one_time_processes(interface)
    __test_range_id_select(interface)
    __test_formats(interface)
    __test_subscriptions(interface)
    __test_job_processes(interface)


# demo code for API module
if __name__ == "__main__":
    willPrint = False
    testing_key_production = "ront0hMeWnTeTqTpVTHcU9qADfiOarqP5cEITaLPmepLgRYGNZr5UZCbUgl1wtiv"
    testing_key_devel = 'a2830DkcQ5KVY8TrjrtpHddvRyjPUfG56xRFoSK0mZlStu001MuuB5dDhKesPQ9y'

    url_devel = "http://hyp3-api-devel.us-west-2.elasticbeanstalk.com/"
    url_local = "http://localhost:5000/"

    crop_to_selection, name, process_id, platform = False, "Hal", 7, "sentinel-1a"
    location = "MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40))," \
        "((20 35, 10 30, 10 10, 30 5, 45 20, 20 35)," \
        "(30 20, 20 15, 20 25, 30 20)))"

    interface = API("wbhorn", api_key=testing_key_devel,
                    url=url_local)

    sub1, sub2 = interface.get_subscription(750), interface.get_subscription(751)
    sub = interface.create_subscription(False, "William", 2, "sentinel-1a",
                                        "/home/william/Documents/shapefiles/MULTIPOLYGON/MULTIPOLYGON_poly.dbf")
    print(sub)
