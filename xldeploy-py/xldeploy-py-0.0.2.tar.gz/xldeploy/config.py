class Config:
    def __init__(self, protocol="http", host="localhost", port="4516", context_path="deployit", username="admin",
                 password="admin", proxy_host=None, proxy_port=None, proxy_username=None, proxy_password=None, verify_ssl=True):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.context_path = context_path
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.verify_ssl = verify_ssl