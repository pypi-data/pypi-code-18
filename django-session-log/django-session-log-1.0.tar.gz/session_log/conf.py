import datetime

from appconf import AppConf
from django.conf import settings

SESSION_IP_KEY = "_activity_ip"
SESSION_LAST_USED_KEY = "_activity_last_used"
SESSION_USER_AGENT_KEY = "_activity_user_agent"
SESSION_ACTIVITY_UPDATE_THROTTLE = datetime.timedelta(minutes=5)

class SessionLogAppConf(AppConf):
    SESSION_ACTIVITY_UPDATE_THROTTLE = datetime.timedelta(minutes=5)

    def configure_update_throttle(self, value):
        if isinstance(value, int):
            value = datetime.timedelta(seconds=value)
        return value
