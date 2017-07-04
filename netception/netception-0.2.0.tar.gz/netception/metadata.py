
class Metadata(object):
    name = "netception"
    version = "0.2.0"
    description = "A neural network inception library"
    author = "Philippe Trempe"
    author_email = "ph.trempe@gmail.com"
    license = "MIT"
    repository_url = "https://github.com/PhTrempe/{}".format(name)
    download_url = "https://github.com/PhTrempe/{}/archive/{}.tar.gz".format(
        name, version)
    keywords = ["neural", "network", "inception", "machine", "learning"]
    requires = ["numpy", "keras"]
