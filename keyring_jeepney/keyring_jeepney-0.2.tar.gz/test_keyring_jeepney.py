import random
from keyring_jeepney import Keyring

def test_basic():
    k = Keyring()
    randno = random.randint(0, 1000)
    service = 'jeepney_keyring_test_%d' % randno
    user = 'sirbedevere'
    pw = 'top_secret_þ_%d' % randno

    k.set_password(service, user, pw)
    print('Set password: %r' % pw)

    retrieved = k.get_password(service, user)
    print('Retrieved password: %r' % retrieved)
    assert retrieved == pw

    k.delete_password(service, user)
    print('Deleted password')
