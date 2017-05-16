from django.conf import settings
import datetime

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'dpauth.utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=6000),
}
