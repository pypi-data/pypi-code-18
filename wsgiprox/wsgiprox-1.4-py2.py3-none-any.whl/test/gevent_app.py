from gevent.monkey import patch_all; patch_all()
from .app import make_application

application = make_application(os.environ.get('CA_ROOT_DIR', '.'))


# ============================================================================
if __name__ == "__main__":
    from gevent.pywsgi import WSGIServer

    WSGIServer(('localhost', 8080), application).serve_forever()


