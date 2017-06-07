'''Modules containing project-wide constants'''

HOST_DEFAULT = 'https://rest.gencove.com'
'''Default backend host'''

DEEPLINK_URL_DEFAULT = 'https://dl.gencove.com/research/{jwt}'
'''Default URL for deeplinking'''

_production_env = {
    'host': HOST_DEFAULT
}

ENVS = {
    'production': _production_env,
    'default': _production_env
}
'''Dictionary containing available environments'''

ENDPOINTS = {
    'register': '/register',
    'login': '/login',
    'logout': '/logout',
    'auth': '/auth',
    'password_change': '/password',
    'password_forgot_init': '/password/forgot',
    'studies': '/studies',
    'study': '/studies/{study_id}',
    'study_participants': '/studies/{study_id}/participants',
    'study_raw_data': '/studies/{study_id}/raw-data',
    'confirm': '/confirm/{confirm_id}',
    'frontend_version_min': '/frontend_version_min'
}
'''Dictionary listing REST endpoints available through API'''

HEADER_JSON = {'Content-Type': 'application/json'}
'''HTTP header template for application/json Content-Type'''
