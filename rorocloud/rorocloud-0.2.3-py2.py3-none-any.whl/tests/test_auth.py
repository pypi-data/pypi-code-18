from rorocloud.auth import FileAuthProvider

class TestFileAuthProvider:
    def test_set_auth(self, tmpdir):
        path = tmpdir.join("rorocloud.conf").strpath
        auth_provider = FileAuthProvider(configfile=path)
        auth_provider.set_auth("test-username", "test-password")

        contents = open(path).read()
        assert 'test-username' in contents
        assert 'test-password' in contents

        auth_provider = FileAuthProvider(configfile=path)
        assert auth_provider.auth == ("test-username", "test-password")
