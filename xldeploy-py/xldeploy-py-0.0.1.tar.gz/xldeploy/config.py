class Config:
    def __init__(self, protocol="http", host="localhost", port="4516", context_path="deployit", username="admin", password="admin"):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.context_path = context_path
