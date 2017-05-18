import flask


def create_auth(providers, onlogin=None, onlogout=None, onauthorized=None):
    auth = flask.Blueprint("auth", __name__)
    for name, provider in providers.items():
        provider.create(auth)

    @auth.route('/login/<provider_name>')
    def login(provider_name):
        if onlogin:
            onlogin(flask.request)

        flask.session["auth_provider"] = provider_name
        return providers[provider_name].login()

    @auth.route('/logout')
    def logout():
        if onlogout:
            onlogout(flask.request)

        provider_name = flask.session["auth_provider"]
        return providers[provider_name].logout()

    @auth.route('/authorized')
    def authorized():
        if onauthorized:
            onauthorized(flask.request)

        provider_name = flask.session["auth_provider"]
        return providers[provider_name].authorized()

    return auth
