#################################################
#         UNIFI PRIVATE CONFIGURATION           #
#################################################

UNIFI_SERVER = "10.0.1.111"; #Change to the IP/FQDN of your UniFi Server
UNIFI_PORT=8443
UNIFI_VERSION='v4'
UNIFI_SITE_ID='default'

#It's important to note that if this server is offsite, you need to have port 8443 forwarded through to it
UNIFI_SSID='ClubLaVela'
UNIFI_LOGO='/static/img/DjangoUnifi.png'

UNIFI_USER = "administrator"; #Change to your UniFi Username
UNIFI_PASSWORD = "P3nt42016!"; #Change to your UniFi Password
UNIFI_TIMEOUT_MINUTES = 60 # 8 hours


# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '628281260704897'
SOCIAL_AUTH_FACEBOOK_SECRET = '61065b7665f39af56289035c221cfa1a'
