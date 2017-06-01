from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import requests

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
env = Environment(
    #loader=PackageLoader('inv_content_list', 'templates'),
    loader = FileSystemLoader('/Users/ChuE/pypi/inv_content_list/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)



URL = 'https://inv999abc.docebosaas.com'
CLIENT_ID = 'acaspike'
CLIENT_SECRET = 'e06504ec7b8e8a8696ccc83f942445d5c2752fcc'

def get_api_token():
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='%s/oauth2/token' % URL,
                              client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET)
    return token['access_token']


def get_course_list():
    post_data = {'access_token': get_api_token()}
    response = requests.post('https://inv999abc.docebosaas.com/api/course/courses', data=post_data)
    content = response.content
    import json
    dct = json.loads(content)
    return dct

def display_content_list(template_file):
    context = get_course_list()['courses']
    template = env.get_template(template_file)
    print template.render(content=context)
