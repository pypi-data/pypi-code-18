import docker

def initialize():
    client = docker.from_env()
    initialize.client = client
    return client
initialize.client = None

def get_containers():
    return initialize.client.containers.list()

def get_services():
    return initialize.client.services.list()
